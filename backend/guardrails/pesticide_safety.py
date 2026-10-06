from agents import Agent, RunContextWrapper, GuardrailFunctionOutput, output_guardrail

BANNED_HAZARDOUS_SUBSTANCES = [
    "ddt", "endosulfan", "methyl parathion", "monocrotophos",
    "paraquat", "aldrin", "dieldrin", "chlordane"
]

HUMAN_MEDICAL_TERMS = [
    "panadol", "paracetamol", "brufen", "disprin", "antibiotic",
    "amoxicillin", "ciprofloxacin", "prescription", "human dosage",
    "doctor prescription", "inject into human", "take orally with water",
    "fever tablet", "painkiller"
]

@output_guardrail
async def pesticide_safety_guardrail(ctx: RunContextWrapper, agent: Agent, output_payload) -> GuardrailFunctionOutput:
    """
    Exit-gate guardrail ensuring agent outputs strictly adhere to agricultural safety standards:
    1. Blocks any human medical diagnosis, painkiller prescriptions, or human pharmaceutical dosages.
    2. Blocks banned or hazardous agricultural chemicals.
    3. Prevents unverified chemical concoction advice.
    """
    output_str = str(output_payload).lower()
    triggered = False
    reason = "Passed agricultural safety verification."

    # 1. Check for human medical terms
    for med in HUMAN_MEDICAL_TERMS:
        if med in output_str:
            triggered = True
            reason = f"Medical safety tripwire triggered: Detected unauthorized human medical reference '{med}'. Kisan Dost provides agronomy advice only."
            break

    # 2. Check for banned/lethal chemicals
    if not triggered:
        for chem in BANNED_HAZARDOUS_SUBSTANCES:
            if chem in output_str:
                triggered = True
                reason = f"Hazardous substance tripwire triggered: '{chem}' is a banned persistent agricultural pollutant."
                break

    return GuardrailFunctionOutput(
        output_info={"reasoning": reason},
        tripwire_triggered=triggered
    )
