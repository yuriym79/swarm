"""Architect agent — system design and technical architecture decisions."""

import importlib.util
import sys
from pathlib import Path

from strands import Agent, tool
from strands_tools import file_read, file_write, editor, http_request

# Load prompts from same directory (handles hyphenated parent dirs)
_prompts_path = Path(__file__).parent / "prompts.py"
_spec = importlib.util.spec_from_file_location("architect_prompts", _prompts_path)
_prompts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_prompts)
ARCHITECT_SYSTEM_PROMPT = _prompts.ARCHITECT_SYSTEM_PROMPT

# Load model config
_models_path = Path(__file__).parent.parent / "models.py"
_mspec = importlib.util.spec_from_file_location("swarm_models", _models_path)
_models = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(_models)


def create_architect_agent(callback_handler=None) -> Agent:
    """Create the architect agent with Claude Opus for deep reasoning."""
    return Agent(
        model=_models.get_architect_model(),
        system_prompt=ARCHITECT_SYSTEM_PROMPT,
        tools=[file_read, file_write, editor, http_request],
        callback_handler=callback_handler,
    )


@tool
def architect(query: str) -> str:
    """Route architecture, system design, database schema, and tech stack questions
    to the architect specialist. Use for: API contract design, database modeling,
    tech stack decisions, integration patterns, and system diagrams."""
    try:
        agent = create_architect_agent()
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in architect agent: {e}"
