import pytest
from bot.services.ai_service import ai_service


def test_detect_topic_programming():
    prompt = "How do I fix this def function syntax error in Python?"
    topic = ai_service.detect_topic(prompt)
    assert topic == "Programming & Code"


def test_detect_topic_math():
    prompt = "Solve the equation 2x + 5 = 15"
    topic = ai_service.detect_topic(prompt)
    assert topic == "Mathematics"


@pytest.mark.asyncio
async def test_ai_generate_response_fallback():
    prompt = "Tell me a joke"
    chunks = []
    async for chunk in ai_service.generate_response(prompt, provider="mock"):
        chunks.append(chunk)

    full_res = "".join(chunks)
    assert "Aria AI" in full_res
    assert prompt in full_res
