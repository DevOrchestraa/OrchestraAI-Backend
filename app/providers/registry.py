from app.providers.gemini import generate_response as gemini_generate_response
from app.providers.groq import generate_response as groq_generate_response


SUPPORTED_PROVIDERS = {
    "gemini": gemini_generate_response,
    "groq": groq_generate_response,
}


def is_valid_provider(provider: str) -> bool:
    return provider.lower() in SUPPORTED_PROVIDERS


def get_provider(provider: str):
    provider = provider.lower()

    if not is_valid_provider(provider):
        raise ValueError(f"Unsupported provider: {provider}")

    return SUPPORTED_PROVIDERS[provider]