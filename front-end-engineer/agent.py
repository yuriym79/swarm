"""Frontend engineer agent — React/Next.js UI development."""

import importlib.util
import sys
from pathlib import Path

from strands import Agent, tool
from strands_tools import file_read, file_write, editor, http_request

_prompts_path = Path(__file__).parent / "prompts.py"
_spec = importlib.util.spec_from_file_location("frontend_prompts", _prompts_path)
_prompts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_prompts)
FRONTEND_ENGINEER_SYSTEM_PROMPT = _prompts.FRONTEND_ENGINEER_SYSTEM_PROMPT

# Load model config
_models_path = Path(__file__).parent.parent / "models.py"
_mspec = importlib.util.spec_from_file_location("swarm_models", _models_path)
_models = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(_models)


def create_frontend_agent(callback_handler=None) -> Agent:
    """Create the frontend engineer agent with local qwen3-coder for UI code."""
    return Agent(
        model=_models.get_frontend_model(),
        system_prompt=FRONTEND_ENGINEER_SYSTEM_PROMPT,
        tools=[file_read, file_write, editor, http_request],
        callback_handler=callback_handler,
    )


@tool
def frontend_engineer(query: str) -> str:
    """Route React, Next.js, CSS, responsive design, and UI component tasks
    to the frontend specialist. Use for: building components, styling, client-side
    state, accessibility, and UI/UX implementation."""
    try:
        agent = create_frontend_agent()
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in frontend agent: {e}"
