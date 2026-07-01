# WellGuard — Well Integrity Monitoring Platform

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-yellow)

Oil & gas well integrity monitoring platform with pressure/temperature analysis, integrity scoring, and real-time alerts.

## Quick Start

```bash
docker compose up -d
```

- Frontend: http://localhost:3000
- API: http://localhost:8000/api/health
- WebSocket: ws://localhost:8000/ws/{user_id}

## Features

- **Well Monitoring** — Register and track oil, gas, and injection wells
- **Pressure & Temp Analysis** — Automated analysis against industry-standard ranges per well type
- **Integrity Scoring** — AI-driven scoring (0–100) based on pressure, temperature, flow rate, and inspection recency
- **Real-Time Alerts** — WebSocket-powered instant alerts for critical/high-risk wells
- **Dashboard** — Stats cards, well list with expandable details, live alert feed

## Architecture

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  React   │◄────│  NGINX   │◄────│  Client  │
│  Frontend│     │  Proxy   │     │  Browser │
└────┬─────┘     └────┬─────┘     └──────────┘
     │ HTTP/WS         │
     ▼                 ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend :8000           │
│  ┌─────┐ ┌──────┐ ┌──────────────────┐ │
│  │Auth │ │CRUD  │ │Integrity Engine  │ │
│  │Router│ │Routers│ │(Analysis Agent)  │ │
│  └──┬──┘ └──┬───┘ └──────────────────┘ │
│     │       │                           │
│  ┌──▼───────▼──────────────────────┐    │
│  │     SQLAlchemy Async ORM        │    │
│  └────────────┬────────────────────┘    │
└───────────────┼─────────────────────────┘
                │
         ┌──────▼──────┐
         │  PostgreSQL  │
         │   Database   │
         └─────────────┘
```

## Tech Stack

| Layer      | Technology                 |
|------------|----------------------------|
| Frontend   | React 18, TypeScript, Vite |
| State      | Zustand                    |
| Charts     | Recharts                   |
| Backend    | Python 3.12, FastAPI       |
| ORM        | SQLAlchemy (async)         |
| Database   | PostgreSQL 16              |
| Auth       | JWT + bcrypt               |
| Real-time  | WebSockets                 |
| Deployment | Docker Compose             |

## API Endpoints

| Method | Endpoint                    | Auth | Description              |
|--------|-----------------------------|------|--------------------------|
| POST   | /api/auth/register          | No   | Register new user        |
| POST   | /api/auth/login             | No   | Login                    |
| POST   | /api/wells                  | Yes  | Create well              |
| GET    | /api/wells                  | Yes  | List wells               |
| GET    | /api/wells/{id}             | Yes  | Get well details         |
| GET    | /api/wells/stats            | Yes  | Get dashboard stats      |
| GET    | /api/alerts                 | Yes  | List alerts              |
| GET    | /api/alerts/stats           | Yes  | Get alert statistics     |
| PATCH  | /api/alerts/{id}/status     | Yes  | Update alert status      |
| WS     | /ws/{user_id}               | No   | Real-time WebSocket      |
| GET    | /api/health                 | No   | Health check             |

## Project Structure

```
WellGuard/
├── backend/
│   ├── app/
│   │   ├── core/          # Config, security, database, deps
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── agents/        # Integrity engine agent
│   │   └── api/           # Route handlers
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── store/         # Zustand stores
│   │   ├── hooks/         # Custom hooks (WebSocket)
│   │   ├── components/    # UI components
│   │   └── pages/         # Route pages
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   └── index.html
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Environment Variables

| Variable       | Default                                                    | Description       |
|----------------|------------------------------------------------------------|-------------------|
| DATABASE_URL   | postgresql+asyncpg://wellguard:wellguard_secret@db:5432/wellguard | PostgreSQL DSN |
| SECRET_KEY     | (set in code for dev)                                      | JWT signing key   |
| ALGORITHM      | HS256                                                      | JWT algorithm     |
| ACCESS_TOKEN_EXPIRE_MINUTES | 60                                               | Token TTL         |

## Demo

1. Open http://localhost:3000
2. Register at `/register`
3. Add wells and trigger integrity analysis

## License

MIT
