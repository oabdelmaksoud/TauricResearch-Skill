from typing import Any, Optional

from .base_client import BaseLLMClient
from .openclaw_client import ChatOpenClawCLI


class OpenClawClient(BaseLLMClient):
    """Client for OpenClaw native agents via CLI."""

    def __init__(self, model: str, base_url: Optional[str] = None, **kwargs):
        super().__init__(model, base_url, **kwargs)

    def get_llm(self) -> Any:
        """Return configured ChatOpenClawCLI instance."""
        
        # The 'model' argument is repurposed as the OpenClaw agent_id
        # Example: 'macro' -> openclaw agent --agent macro
        llm_kwargs = {"agent_id": self.model}

        for key in ("timeout",):
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        return ChatOpenClawCLI(**llm_kwargs)

    def validate_model(self) -> bool:
        """
        Validate model for OpenClaw. For this adapter, we assume any string
        passed in (e.g., 'macro', 'pulse') is a valid OpenClaw agent ID.
        """
        return True
