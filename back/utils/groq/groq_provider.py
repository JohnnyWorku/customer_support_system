import os
import time
import httpx
from typing import List, Optional, Dict, Any, Union
from back.utils.groq.base import BaseLLMProvider, LLMResult, TokenUsage, Message

class GroqProvider(BaseLLMProvider):
    def __init__(self, model_name):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable not set")
        # self.model_name = "llama-3.1-8b-instant"
        self.model_name = model_name
        self.provider_name = "groq"
        self.max_retries = 3
        self.client = httpx.Client(
            base_url="https://api.groq.com/openai/v1",
            timeout=60,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )

    def generate_response(
        self,
        messages: Union[str, List[Message]],
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> LLMResult:
        if isinstance(messages, str):
            prepared: List[Message] = [{"role": "user", "content": messages}]
        else:
            prepared = list(messages)
        if system:
            prepared = [{"role": "system", "content": system}] + prepared

        selected_model = model or self.model_name
        payload: Dict[str, Any] = {
            "model": selected_model,
            "messages": prepared,
            "temperature": 0.7 if temperature is None else temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        payload.update(kwargs)

        last_err: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                response = self.client.post("chat/completions", json=payload)
                if response.status_code == 429 and attempt < self.max_retries - 1:
                    time.sleep(int(response.headers.get("Retry-After", "2")))
                    continue
                response.raise_for_status()
                data = response.json()
                text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                usage = data.get("usage", {}) or {}
                return LLMResult(
                    text=text,
                    usage=TokenUsage(
                        input_tokens=int(usage.get("prompt_tokens", 0)),
                        output_tokens=int(usage.get("completion_tokens", 0)),
                    ),
                    provider=self.provider_name,
                    model=data.get("model") or selected_model,
                    raw=data,
                )
            except httpx.HTTPStatusError as e:
                last_err = e
                status = e.response.status_code if e.response is not None else "unknown"
                body = e.response.text if e.response is not None else ""
                if attempt < self.max_retries - 1 and status in (429, 500, 502, 503, 504):
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"Groq API error (status={status}): {body or str(e)}") from e
            except Exception as e:
                last_err = e
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"Groq generate failed: {e}") from e
        raise RuntimeError(f"Groq generate failed after retries: {last_err}")
