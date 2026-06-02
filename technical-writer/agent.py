"""Technical writer agent — documentation and guides."""

import importlib.util
import sys
from pathlib import Path

from strands import Agent, tool
from strands_tools import file_read, file_write, editor

_prompts_path = Path(__file__).parent / "prompts.py"
_spec = importlib.util.spec_from_file_location("writer_prompts", _prompts_path)
_prompts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_prompts)
TECHNICAL_WRITER_SYSTEM_PROMPT = _prompts.TECHNICAL_WRITER_SYSTEM_PROMPT

# Load model config
_models_path = Path(__file__).parent.parent / "models.py"
_mspec = importlib.util.spec_from_file_location("swarm_models", _models_path)
_models = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(_models)


def create_writer_agent(callback_handler=None) -> Agent:
    """Create the technical writer agent with Claude Sonnet (higher temp for prose)."""
    return Agent(
        model=_models.get_writer_model(),
        system_prompt=TECHNICAL_WRITER_SYSTEM_PROMPT,
        tools=[file_read, file_write, editor],
        callback_handler=callback_handler,
    )


@tool
def technical_writer(query: str) -> str:
    """Route documentation, README, API docs, and guide writing tasks to the
    technical writer specialist. Use for: API reference docs, setup guides,
    deployment runbooks, and architecture decision records."""
    try:
        agent = create_writer_agent()
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in technical writer agent: {e}"
