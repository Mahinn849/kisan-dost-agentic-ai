import asyncio
from backend.guardrails.pesticide_safety import pesticide_safety_guardrail
from backend.guardrails.input_guardrail import agriculture_input_guardrail

class MockContext:
    context = {}

class MockAgent:
    pass

def test_guardrail_blocks_human_medicine():
    """Tests that output guardrail trips wire on human medicine recommendations."""
    bad_output = "Apply 2 tablets of panadol with water."
    res = asyncio.run(pesticide_safety_guardrail.guardrail_function(MockContext(), MockAgent(), bad_output))
    assert res.tripwire_triggered is True
    assert "panadol" in res.output_info["reasoning"]

def test_guardrail_blocks_banned_chemicals():
    """Tests that output guardrail trips wire on banned toxic chemical DDT."""
    bad_chem = "Spray DDT 50 WP directly on cotton crops."
    res = asyncio.run(pesticide_safety_guardrail.guardrail_function(MockContext(), MockAgent(), bad_chem))
    assert res.tripwire_triggered is True
    assert "banned" in res.output_info["reasoning"].lower() or "ddt" in res.output_info["reasoning"].lower()

def test_guardrail_allows_safe_agronomy_advice():
    """Tests that safe agricultural output passes without tripwire."""
    safe_output = "Apply Diafenthiuron 500 SC at 200-250 ml per acre in 100 liters of water during early morning."
    res = asyncio.run(pesticide_safety_guardrail.guardrail_function(MockContext(), MockAgent(), safe_output))
    assert res.tripwire_triggered is False

def test_input_guardrail_quick_pass():
    """Tests that common farming prompts quickly pass input guardrail."""
    res = asyncio.run(agriculture_input_guardrail.guardrail_function(MockContext(), MockAgent(), "Multan mein wheat ka mandi rate kya hai?"))
    assert res.tripwire_triggered is False
