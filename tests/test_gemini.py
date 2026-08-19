import os
import pytest
from dotenv import load_dotenv

from app.providers.gemini import generate_response
from app.providers.exceptions import ProviderError

load_dotenv()

@pytest.mark.anyio
async def test_generate_response():

    api_key = os.getenv('GEMINI_API_KEY')

    response = await generate_response(
        api_key=api_key,
        prompt="Hello Gemini,This ia a test prompt",
        model='gemini-3.5-flash',
        max_tokens=50,
    )

    assert "response" in response
    assert "model" in response
    assert "provider" in response
    assert "usage" in response
    assert "finish_reason" in response
    assert response["provider"] == 'gemini'
    assert response["model"] == 'gemini-3.5-flash'

@pytest.mark.anyio
async def test_generate_response_error():
    api_key = os.getenv("GEMINI_API_KEY")

    with pytest.raises(ProviderError):
        await generate_response(
            api_key=api_key,
            prompt="Hello",
            model="invalid-model-name",
            max_tokens=50,
        )
