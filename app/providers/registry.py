from app.providers.groq import generate_response


SUPPORTED_PROVIDERS = {
    "groq": generate_response,
}


def is_valid_provider(provider: str) -> bool:
    return provider.lower() in SUPPORTED_PROVIDERS


def get_provider(provider: str):
    provider = provider.lower()

    if not is_valid_provider(provider):
        raise ValueError(f"Unsupported provider: {provider}")

    return SUPPORTED_PROVIDERS[provider]