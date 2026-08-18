import os
import pytest
from dotenv import load_dotenv

from app.providers.groq import generate_response
from app.providers.exceptions import ProviderError
from app.providers.registry import is_valid_provider
from app.providers.registry import get_provider


load_dotenv()


def test_generate_response():

    api_key = os.getenv("GROQ_API_KEY")

    response = generate_response(
        api_key=api_key,
        prompt="Hello Groq, this is a test prompt",
        model="qwen/qwen3.6-27b",
        max_tokens=50,
    )

    assert "response" in response
    assert "model" in response
    assert "provider" in response
    assert "usage" in response
    assert "finish_reason" in response

    assert response["provider"] == "groq"
    assert response["model"] == "qwen/qwen3.6-27b"

def test_generate_response_error():
    api_key = os.getenv("GROQ_API_KEY")

    with pytest.raises(ProviderError):
        generate_response(
            api_key=api_key,
            prompt="Hello",
            model="invalid-model-name",
            max_tokens=50,
        )

def test_valid_provider():
    assert is_valid_provider("groq") is True
    assert is_valid_provider("Groq") is True
    assert is_valid_provider("openai") is False
    assert is_valid_provider("random") is False

def test_get_provider():
    provider = get_provider("groq")

    assert provider is generate_response

def test_get_invalid_provider():
    with pytest.raises(ValueError):
        get_provider("openai")

def test_provider_can_be_called():

    api_key = os.getenv("GROQ_API_KEY")

    provider = get_provider("groq")

    response = provider(
        api_key=api_key,
        prompt="Say hello in one sentence.",
        model="qwen/qwen3.6-27b",
        max_tokens=50,
    )

    assert response["provider"] == "groq"
    assert response["response"]