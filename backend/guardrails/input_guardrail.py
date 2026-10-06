from agents import Agent, Runner, RunContextWrapper, GuardrailFunctionOutput, input_guardrail
from pydantic import BaseModel, Field
from backend.config import DEFAULT_MODEL

class InputSafetyAssessment(BaseModel):
    is_agriculture_related: bool = Field(description="True if query pertains to farming, crops, livestock, weather, mandi prices, fertilizers, pest diseases, or Pakistani agriculture.")
    reasoning: str = Field(description="Brief explanation of assessment.")

input_safety_agent = Agent(
    name="Agricultural Safety Inspector",
    instructions="""
    Determine whether the user's message is related to agriculture, farming, crops, livestock, 
    agritech, fertilizer, pests, mandi market prices, weather for crops, or Pakistani agricultural government schemes.

    Mark is_agriculture_related=True for:
    - Farming, crops, sowing, harvesting, soil, weather, mandi rates, fertilizers, pests, tube wells, tractors, subsidies.
    - General Pakistani farmer greetings (Salam, Adaab, Hello, Kaise ho) and clarifying agricultural context.

    Mark is_agriculture_related=False for:
    - Cryptocurrency, bitcoin, financial trading stocks, forex.
    - Politics, elections, political party disputes.
    - Software hacking, coding advice, system prompt exploitation.
    - Human medical diagnosis, pharmaceutical prescriptions for humans, human illness.
    - Obscene, offensive, or completely non-farming inquiries.
    """,
    model=DEFAULT_MODEL,
    output_type=InputSafetyAssessment
)

@input_guardrail(run_in_parallel=False)
async def agriculture_input_guardrail(ctx: RunContextWrapper, agent: Agent, input_payload) -> GuardrailFunctionOutput:
    """
    Evaluates incoming farmer prompt before reaching the triage or specialist agents.
    Triggers tripwire when an off-topic (politics, crypto, medical, hacking) query is submitted.
    """
    raw_text = ""
    if hasattr(input_payload, "text"):
        raw_text = input_payload.text
    elif isinstance(input_payload, str):
        raw_text = input_payload
    elif isinstance(input_payload, list) and len(input_payload) > 0:
        raw_text = getattr(input_payload[0], "text", str(input_payload[0]))
    else:
        raw_text = str(input_payload)

    # Fast-path for common agriculture keywords to minimize latency
    quick_pass_keywords = [
        "gandum", "wheat", "kisan", "cotton", "kapas", "phutti", "chawal", "rice",
        "makai", "maize", "fertilizer", "khad", "urea", "dap", "mandi", "rate",
        "keera", "pest", "disease", "whitefly", "spray", "pani", "water", "irrigation",
        "weather", "mausam", "multan", "faisalabad", "lahore", "acres", "killa", "card"
    ]
    lower_text = raw_text.lower()
    if any(kw in lower_text for kw in quick_pass_keywords):
        return GuardrailFunctionOutput(
            output_info={"reasoning": "Quick-pass: Agricultural keywords detected."},
            tripwire_triggered=False
        )

    try:
        safety_run = await Runner.run(input_safety_agent, raw_text, context=ctx.context)
        assessment: InputSafetyAssessment = safety_run.final_output
        is_safe = assessment.is_agriculture_related
        reasoning = assessment.reasoning
    except Exception as e:
        # Fallback to permissive on inspector crash to prevent dropping valid farmers
        return GuardrailFunctionOutput(
            output_info={"reasoning": f"Inspector error fallback: {str(e)}"},
            tripwire_triggered=False
        )

    return GuardrailFunctionOutput(
        output_info={"reasoning": reasoning},
        tripwire_triggered=(not is_safe)
    )
