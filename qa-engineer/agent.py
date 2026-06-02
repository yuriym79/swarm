"""QA engineer agent — testing strategy and automation."""

import importlib.util
import sys
from pathlib import Path

from strands import Agent, tool
from strands_tools import file_read, file_write, editor, http_request

_prompts_path = Path(__file__).parent / "prompts.py"
_spec = importlib.util.spec_from_file_location("qa_prompts", _prompts_path)
_prompts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_prompts)
QA_ENGINEER_SYSTEM_PROMPT = _prompts.QA_ENGINEER_SYSTEM_PROMPT

# Load model config
_models_path = Path(__file__).parent.parent / "models.py"
_mspec = importlib.util.spec_from_file_location("swarm_models", _models_path)
_models = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(_models)


def create_qa_agent(callback_handler=None) -> Agent:
    """Create the QA agent with local qwen3-coder for test code generation."""
    return Agent(
        model=_models.get_qa_model(),
        system_prompt=QA_ENGINEER_SYSTEM_PROMPT,
        tools=[file_read, file_write, editor, http_request],
        callback_handler=callback_handler,
    )


@tool
def qa_engineer(query: str) -> str:
    """Route testing, quality assurance, and bug investigation tasks to the QA
    specialist. Use for: writing tests, test plans, code review from quality
    perspective, and debugging test failures."""
    try:
        agent = create_qa_agent()
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in QA agent: {e}"
