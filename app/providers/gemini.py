from google import genai
from app.providers.exceptions import ProviderError

async def generate_response(api_key: str, prompt: str, model: str, max_tokens: int) -> dict:


    try:
        client = genai.Client(api_key=api_key)

        response = await client.aio.models.generate_content(
            model = model,
            contents = prompt,
            config={
                "max_output_tokens": max_tokens,
            },
        )

        usage = response.usage_metadata
        return {
                "response": response.text,
                "model": model,
                "provider":'gemini',

                "usage": {
                    "prompt_tokens": usage.prompt_token_count,
                    "completion_tokens": usage.total_token_count - usage.prompt_token_count,
                    "total_tokens": usage.total_token_count,
                },
                "finish_reason": (
                    response.candidates[0].finish_reason.name
                    if response.candidates
                    else None
                ),
            }

    except Exception as e:
        raise ProviderError(str(e)) from e

    finally:
        await client.aio.aclose()
