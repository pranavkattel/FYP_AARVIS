# final_fyp_aarvis

Smart mirror assistant project.

## Quick start

```bash
python -m final_fyp_aarvis.main
```

## Core files

1. `final_fyp_aarvis/main.py`
	- Server startup.

2. `final_fyp_aarvis/api/server.py`
	- FastAPI routes and WebSocket logic.

3. `final_fyp_aarvis/agent/graph.py`
	- Agent flow (LLM + tools).

4. `final_fyp_aarvis/agent/tools.py`
	- Calendar, weather, news, and email tools.

5. `final_fyp_aarvis/database/repository.py`
	- Database operations (users, conversation history, OAuth tokens).

## Other folders (use when needed)

- `final_fyp_aarvis/services/`: Integrations (Gmail, Google OAuth, TTS, STT, calendar).
- `final_fyp_aarvis/models/`: Request models.
- `final_fyp_aarvis/templates/`, `final_fyp_aarvis/static/`: Frontend files.
- `final_fyp_aarvis/tests/`: Test files.
