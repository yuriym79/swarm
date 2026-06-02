"""Security engineer agent — auth flows and vulnerability prevention."""

import importlib.util
import sys
from pathlib import Path

from strands import Agent, tool
from strands_tools import file_read, file_write, editor, http_request

_prompts_path = Path(__file__).parent / "prompts.py"
_spec = importlib.util.spec_from_file_location("security_prompts", _prompts_path)
_prompts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_prompts)
SECURITY_ENGINEER_SYSTEM_PROMPT = _prompts.SECURITY_ENGINEER_SYSTEM_PROMPT

# Load model config
_models_path = Path(__file__).parent.parent / "models.py"
_mspec = importlib.util.spec_from_file_location("swarm_models", _models_path)
_models = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(_models)


def create_security_agent(callback_handler=None) -> Agent:
    """Create the security agent with Claude Opus for deep threat analysis."""
    return Agent(
        model=_models.get_security_model(),
        system_prompt=SECURITY_ENGINEER_SYSTEM_PROMPT,
        tools=[file_read, file_write, editor, http_request],
        callback_handler=callback_handler,
    )


@tool
def security_engineer(query: str) -> str:
    """Route authentication, authorization, security headers, and vulnerability
    prevention tasks to the security specialist. Use for: auth middleware, CSP
    headers, CSRF protection, input sanitization, and security code review."""
    try:
        agent = create_security_agent()
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in security agent: {e}"
