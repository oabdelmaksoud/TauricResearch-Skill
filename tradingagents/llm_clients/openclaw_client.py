from typing import Any, List, Optional, Dict
import subprocess
import json
import logging

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, ChatMessage
from langchain_core.outputs import ChatResult, ChatGeneration

logger = logging.getLogger(__name__)

class ChatOpenClawCLI(BaseChatModel):
    """
    A custom LangChain adapter that routes LLM requests through the OpenClaw CLI.
    This allows the TauricResearch LangGraph to remain fully intact while honoring
    the requirement that 100% of LLM execution runs natively via the `openclaw` shell command.
    """
    
    agent_id: str
    """The ID of the OpenClaw agent to invoke (e.g., 'trading_analyst', 'debate_judge')"""
    
    timeout: int = 240
    """Subprocess timeout in seconds."""
    
    @property
    def _llm_type(self) -> str:
        return "openclaw_cli"
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Intercepts the graph's LLM call, stringifies the message history, 
        and ferries it out to the OpenClaw CLI.
        """
        # 1. Format the conversation history for the CLI prompt
        prompt = self._format_messages_to_prompt(messages)
        return self._call_openclaw_cli(prompt)

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Async version of _generate."""
        # For simplicity in the CLI wrapper, we just call the sync version.
        # In a high-throughput production environment, this could be refactored 
        # to use asyncio.create_subprocess_exec.
        return self._generate(messages, stop, run_manager, **kwargs)

    def _format_messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        """Flattens the LangChain conversational history into a single string prompt."""
        formatted_prompt = ""
        for msg in messages:
            role = msg.type
            if isinstance(msg, ChatMessage):
                role = msg.role
            formatted_prompt += f"{role.upper()}:\n{msg.content}\n\n"
        return formatted_prompt.strip()

    def _call_openclaw_cli(self, prompt: str) -> ChatResult:
        """Executes the `openclaw agent` CLI and parses the JSON output."""
        
        command = [
             "openclaw", 
             "agent", 
             "--agent", self.agent_id, 
             "--message", prompt,
             "--json"
        ]
        
        logger.info(f"Calling OpenClaw CLI for agent: '{self.agent_id}'")
        
        try:
            # Execute the CLI
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                timeout=self.timeout
            )
            
            # The CLI might output non-JSON warnings to stdout. We must extract 
            # the JSON object safely.
            output_str = result.stdout
            
            start_idx = output_str.find('{')
            end_idx = output_str.rfind('}')
            
            if start_idx == -1 or end_idx == -1:
                logger.error(f"OpenClaw CLI did not return JSON. Stderr: {result.stderr}")
                raise ValueError("Failed to extract JSON from OpenClaw CLI output.")
                
            json_str = output_str[start_idx:end_idx + 1]
            data = json.loads(json_str)
            
            # The expected OpenClaw schema is result.payloads[0].text
            payloads = data.get("result", {}).get("payloads", [])
            if not payloads:
                 raise ValueError("JSON parsed successfully but 'payloads' array is empty.")
                 
            content = payloads[0].get("text", "")
            
            # Return as a native LangChain ChatResult so the Graph can continue
            message = AIMessage(content=content)
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])
            
        except subprocess.TimeoutExpired:
            logger.error(f"OpenClaw CLI timed out after {self.timeout} seconds.")
            raise
        except Exception as e:
            logger.error(f"Error executing OpenClaw CLI for agent {self.agent_id}: {str(e)}")
            raise
