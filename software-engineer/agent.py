"""Backend/software engineer agent — API and business logic."""

import importlib.util
import sys
from pathlib import Path

from strands import Agent, tool
from strands_tools import file_read, file_write, editor, http_request

_prompts_path = Path(__file__).parent / "prompts.py"
_spec = importlib.util.spec_from_file_location("backend_prompts", _prompts_path)
_prompts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_prompts)
BACKEND_ENGINEER_SYSTEM_PROMPT = _prompts.BACKEND_ENGINEER_SYSTEM_PROMPT

# Load model config
_models_path = Path(__file__).parent.parent / "models.py"
_mspec = importlib.util.spec_from_file_location("swarm_models", _models_path)
_models = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(_models)


def create_backend_agent(callback_handler=None) -> Agent:
    """Create the backend engineer agent with local qwen3-coder for API code.

    Args:
        callback_handler: Optional callback for observability.
            Use verbose_handler or minimal_handler from callbacks.py.
    """
    return Agent(
        model=_models.get_backend_model(),
        system_prompt=BACKEND_ENGINEER_SYSTEM_PROMPT,
        tools=[file_read, file_write, editor, http_request],
        callback_handler=callback_handler,
    )


@tool
def backend_engineer(query: str) -> str:
    """Route API endpoint, database query, server logic, and integration tasks
    to the backend specialist. Use for: Express routes, Prisma queries, Stripe
    integration, email sending, and input validation."""
    try:
        agent = create_backend_agent()
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in backend agent: {e}"
