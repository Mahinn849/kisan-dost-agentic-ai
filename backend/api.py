import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from agents import Runner, SQLiteSession
from agents.exceptions import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from backend.config import DB_PATH, BASE_DIR
from backend.agents import main_triage_agent
from backend.models.context_models import FarmerProfile

app = FastAPI(title="Kisan Dost Agronomy Platform", version="1.0.0")

# Locate templates directory in frontend
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
if not TEMPLATES_DIR.exists():
    TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Multi-turn persistent session
web_session = SQLiteSession(
    session_id="kisan_dost_web_user",
    db_path=DB_PATH
)
web_profile = FarmerProfile()

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    """Serves the professional agricultural white dashboard frontend."""
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    """
    Receives chat message from frontend and executes multi-agent runner.
    """
    payload = await request.json()
    user_message = payload.get("message", "").strip()

    if not user_message:
        return {"reply": "Barah-e-karam apna sawaal likhein."}

    try:
        result = await Runner.run(
            main_triage_agent,
            user_message,
            session=web_session,
            context=web_profile
        )
        return {"reply": str(result.final_output)}

    except InputGuardrailTripwireTriggered:
        return {
            "reply": "⚠️ [Input Guardrail Block]: Yeh sawaal ziraat (agriculture) se mutaliq nahi hai. Barah-e-karam sirf faslon, khad, mausam, beemari, ya mandi rates ke bare mein poochein."
        }

    except OutputGuardrailTripwireTriggered:
        return {
            "reply": "🛡️ [Pesticide Safety Guardrail Block]: System ne unverified chemical ya insani dawa ki hidayat ko safety ke teht rok diya hai. Barah-e-karam apne qareebi Agriculture Extension officer se mashwara karein."
        }

    except Exception as e:
        return {"reply": f"⚠️ System encountered a connection fault: {str(e)}"}
