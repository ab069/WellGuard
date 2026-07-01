from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json

from app.core.database import get_db, async_session_factory
from app.models.well import Well
from app.agents.integrity_engine import (
    analyze_well_pressure,
    analyze_temperature,
    calculate_integrity_score,
    generate_well_report,
)
from app.services.alert_service import create_alert

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_message(self, user_id: str, message: dict):
        ws = self.active_connections.get(user_id)
        if ws:
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(user_id)


manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            action = payload.get("action")

            if action == "analyze":
                well_id = payload.get("well_id")
                if not well_id:
                    await manager.send_message(user_id, {"type": "error", "message": "well_id required"})
                    continue

                async with async_session_factory() as db:
                    result = await db.execute(select(Well).where(Well.id == well_id, Well.user_id == user_id))
                    well = result.scalar_one_or_none()
                    if not well:
                        await manager.send_message(user_id, {"type": "error", "message": "Well not found"})
                        continue

                    days_since_inspection = 365
                    if well.last_inspected:
                        delta = well.last_inspected - well.created_at
                        days_since_inspection = max(0, delta.days)

                    pressure_result = analyze_well_pressure(well.pressure, well.depth, well.well_type)
                    temp_result = analyze_temperature(well.temperature, well.well_type)
                    score = calculate_integrity_score(
                        pressure_result["risk"],
                        temp_result["risk"],
                        well.flow_rate,
                        days_since_inspection,
                    )
                    report = generate_well_report(well.well_name, score, [pressure_result, temp_result])

                    well.integrity_score = score
                    await db.commit()

                    if pressure_result["risk"] in ("critical", "high") or temp_result["risk"] in ("critical", "high"):
                        severity = "critical" if pressure_result["risk"] == "critical" or temp_result["risk"] == "critical" else "high"
                        alert = await create_alert(
                            db, user_id, well_id,
                            title=f"{well.well_name} - {severity.title()} Integrity Risk",
                            severity=severity,
                            description=report,
                        )
                        await manager.send_message(user_id, {
                            "type": "alert",
                            "alert": alert.model_dump(),
                        })

                    await manager.send_message(user_id, {
                        "type": "analysis_result",
                        "well_id": well_id,
                        "integrity_score": score,
                        "pressure_risk": pressure_result,
                        "temperature_risk": temp_result,
                        "report": report,
                    })

            elif action == "ping":
                await manager.send_message(user_id, {"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception:
        manager.disconnect(user_id)
