from groq import Groq
from app.providers.exceptions import ProviderError

def generate_response(api_key: str, prompt: str, model: str, max_tokens: int) -> dict : 

    client = Groq(api_key = api_key)
    try:
        response = client.chat.completions.create(
            model = model,
            messages = [
                {"role": "user",
                "content": prompt}
            ],
            max_tokens = max_tokens
        )
    except Exception as e:
        raise ProviderError(str(e)) from e
    return {
        "response": response.choices[0].message.content,
        "model":response.model,
        "provider":'groq',
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        "finish_reason": response.choices[0].finish_reason,
    }