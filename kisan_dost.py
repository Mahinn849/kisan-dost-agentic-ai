"""
Kisan Dost Main Unified Entrypoint.
Routes cleanly to backend multi-agent architecture and launches Terminal CLI or Web Dashboard.
"""
import sys
from backend.agents.triage_agent import main_triage_agent as main_agent
from backend.api import app

if __name__ == "__main__":
    if "--web" in sys.argv:
        import uvicorn
        print("🌾 Starting Kisan Dost Web Dashboard on http://127.0.0.1:8000...")
        uvicorn.run("backend.api:app", host="127.0.0.1", port=8000, reload=False)
    else:
        from run_cli import main
        main()
