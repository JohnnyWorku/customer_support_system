from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union

Message = Dict[str, str]  # {"role": "user"/"assistant"/"system", "content": "..."}


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0


@dataclass(frozen=True)
class LLMResult:
    text: str
    usage: TokenUsage
    provider: str
    model: str
    raw: Optional[Dict[str, Any]] = None


class BaseLLMProvider(ABC):
    @abstractmethod
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
        raise NotImplementedError
