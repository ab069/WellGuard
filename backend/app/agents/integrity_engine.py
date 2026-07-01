from datetime import datetime, timezone


PRESSURE_RANGES = {
    "oil": {"min": 500, "max": 5000, "optimal_min": 1000, "optimal_max": 3500},
    "gas": {"min": 300, "max": 8000, "optimal_min": 800, "optimal_max": 5000},
    "injection": {"min": 1000, "max": 10000, "optimal_min": 2000, "optimal_max": 7000},
}

TEMP_RANGES = {
    "oil": {"min": 20, "max": 150, "optimal_min": 40, "optimal_max": 100},
    "gas": {"min": -20, "max": 120, "optimal_min": 10, "optimal_max": 80},
    "injection": {"min": 5, "max": 200, "optimal_min": 20, "optimal_max": 120},
}

FLOW_RATE_RANGES = {
    "oil": {"min": 0, "max": 50000, "optimal_min": 500, "optimal_max": 20000},
    "gas": {"min": 0, "max": 1000000, "optimal_min": 10000, "optimal_max": 500000},
    "injection": {"min": 0, "max": 100000, "optimal_min": 1000, "optimal_max": 50000},
}


def analyze_well_pressure(pressure: float, depth: float, well_type: str) -> dict:
    ranges = PRESSURE_RANGES.get(well_type, PRESSURE_RANGES["oil"])
    expected = ranges["min"] + (depth * 0.15)
    deviation_pct = ((pressure - expected) / expected) * 100 if expected > 0 else 0

    if pressure < ranges["min"] or pressure > ranges["max"]:
        if deviation_pct < -30 or deviation_pct > 30:
            risk = "critical"
        else:
            risk = "high"
    elif pressure < ranges["optimal_min"] or pressure > ranges["optimal_max"]:
        risk = "medium" if abs(deviation_pct) > 10 else "low"
    else:
        risk = "normal"

    return {
        "risk": risk,
        "pressure": pressure,
        "expected_pressure": round(expected, 1),
        "deviation_pct": round(deviation_pct, 1),
        "message": f"Pressure {pressure} psi is {risk} for {well_type} well at depth {depth} ft",
    }


def analyze_temperature(temperature: float, well_type: str) -> dict:
    ranges = TEMP_RANGES.get(well_type, TEMP_RANGES["oil"])

    if temperature < ranges["min"] or temperature > ranges["max"]:
        risk = "critical" if abs(temperature - ranges["min"]) > 20 or abs(temperature - ranges["max"]) > 20 else "high"
    elif temperature < ranges["optimal_min"] or temperature > ranges["optimal_max"]:
        risk = "medium"
    else:
        risk = "normal"

    return {
        "risk": risk,
        "temperature": temperature,
        "optimal_range": [ranges["optimal_min"], ranges["optimal_max"]],
        "message": f"Temperature {temperature}°C is {risk} for {well_type} well",
    }


def calculate_integrity_score(pressure_risk: str, temp_risk: str, flow_rate: float, days_since_inspection: int) -> int:
    score = 100

    risk_penalties = {
        "critical": 30,
        "high": 20,
        "medium": 10,
        "low": 5,
        "normal": 0,
    }

    score -= risk_penalties.get(pressure_risk, 0)
    score -= risk_penalties.get(temp_risk, 0)

    if days_since_inspection > 365:
        score -= 15
    elif days_since_inspection > 180:
        score -= 10
    elif days_since_inspection > 90:
        score -= 5

    score -= max(0, flow_rate / 10000)

    return max(0, min(100, int(round(score))))


def generate_well_report(well_name: str, score: int, findings: list[dict]) -> str:
    if score >= 80:
        status = "GOOD"
        recommendation = "Routine monitoring is sufficient."
    elif score >= 50:
        status = "FAIR"
        recommendation = "Schedule inspection within 30 days."
    else:
        status = "POOR"
        recommendation = "Immediate inspection and intervention required."

    findings_text = "\n".join(f"- {f.get('message', str(f))}" for f in findings)

    return (
        f"Well Integrity Report: {well_name}\n"
        f"Overall Status: {status}\n"
        f"Integrity Score: {score}/100\n"
        f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n"
        f"Findings:\n{findings_text}\n\n"
        f"Recommendation: {recommendation}"
    )
