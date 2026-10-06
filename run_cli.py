import asyncio
import sys
from agents import Runner, SQLiteSession
from backend.config import DB_PATH
from backend.agents import main_triage_agent
from backend.models.context_models import FarmerProfile
from agents.exceptions import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered

# Ensure Windows terminal prints UTF-8 / Urdu properly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BANNER = """
========================================================================
🌾  KISAN DOST (کسان دوست) — 24/7 AI Agronomy Advisory Terminal
    Built with OpenAI Agents SDK • Terminal Agent Challenge
========================================================================
Available Specialist Agents:
  🌱 Agronomy Agent    : Crop recommendations, Rabi/Kharif, Fertilizer NPK
  🐛 Pest Doctor Agent : Leaf diseases, Whitefly, Rust, IPM & Safe dosages
  📊 Market Agent      : Live AMIS Mandi prices, Punjab Govt Kisan Card
  💰 Finance Agent     : Full season crop budget, Net profit & Break-even
  🌦️  Weather Agent     : Open-Meteo live forecast, Rain & Frost alerts

Type 'exit', 'quit', or 'q' to end the session.
========================================================================
"""

async def run_terminal_session():
    print(BANNER)

    # Initialize persistent session for conversation memory
    session = SQLiteSession(
        session_id="kisan_dost_terminal",
        db_path=DB_PATH
    )

    # In-memory typed farmer profile context
    farmer_profile = FarmerProfile()

    current_agent = main_triage_agent

    while True:
        try:
            print("\n🧑‍🌾 Farmer (Aap): ", end="", flush=True)
            user_input = sys.stdin.readline()
            if not user_input:
                break

            user_text = user_input.strip()
            if not user_text:
                continue

            if user_text.lower() in ["exit", "quit", "q", "khatam"]:
                print("\n🌾 Shukriya! Kisan Dost ke sath rabta karne ka shukriya. Allah aap ki fasal mein barkat de! Khuda Hafiz.\n")
                break

            print("\n🤖 Kisan Dost soch raha hai...", flush=True)

            try:
                # Run through OpenAI Agents SDK Runner
                result = await Runner.run(
                    current_agent,
                    user_text,
                    session=session,
                    context=farmer_profile
                )

                # Track active agent across handoffs
                if hasattr(result, "agent") and result.agent:
                    current_agent = result.agent

                active_agent_name = getattr(current_agent, "name", "Kisan Dost")

                print(f"\n[{active_agent_name}]:")
                print("-" * 65)
                print(result.final_output)
                print("-" * 65)

            except InputGuardrailTripwireTriggered:
                print("\n⚠️ [Kisan Dost Guardrail]:")
                print("Mohtaram Kisan Bhai, yeh sawaal ziraat ya faslon ke mutaliq nahi hai. Barah-e-karam sirf kheti-baari, khad, mandi rates, ya fasli beemariyon ke bare mein poochein.")

            except OutputGuardrailTripwireTriggered:
                print("\n🛡️ [Pesticide Safety Guardrail Block]:")
                print("System ne ghair tasdeeq shuda ya insani dawa se mutaliq hidayat ko safety ke teht rok diya hai. Barah-e-karam ziraat ke maahir se tasdeeq karein.")

            except Exception as e:
                print(f"\n⚠️ [System Error]: Muazrat, rabtay mein rukawat aayi: {str(e)}")

        except (KeyboardInterrupt, EOFError):
            print("\n\nSession terminated. Khuda Hafiz!\n")
            break

def main():
    try:
        asyncio.run(run_terminal_session())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
