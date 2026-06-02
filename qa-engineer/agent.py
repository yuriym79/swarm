"""QA engineer agent — testing strategy and automation."""

import importlib.util
import os
from pathlib import Path

from strands import Agent, tool
from strands_tools import file_read, file_write, editor, http_request

_prompts_path = Path(__file__).parent / "prompts.py"
_spec = importlib.util.spec_from_file_location("qa_prompts", _prompts_path)
_prompts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_prompts)
QA_ENGINEER_SYSTEM_PROMPT = _prompts.QA_ENGINEER_SYSTEM_PROMPT

_models_path = Path(__file__).parent.parent / "models.py"
_mspec = importlib.util.spec_from_file_location("swarm_models", _models_path)
_models = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(_models)

_context_path = Path(__file__).parent.parent / "context.py"
_cspec = importlib.util.spec_from_file_location("swarm_context", _context_path)
_context_mod = importlib.util.module_from_spec(_cspec)
_cspec.loader.exec_module(_context_mod)

PROJECT_ROOT = os.environ.get(
    "HEADSTASH_ROOT",
    "c:/Users/yuriy/OneDrive/Desktop/KiroProjects/headstash-website"
)


def create_qa_agent(callback_handler=None) -> Agent:
    """Create the QA agent with local qwen3-coder for test code generation."""
    project_context = _context_mod.get_project_context(PROJECT_ROOT)
    full_prompt = QA_ENGINEER_SYSTEM_PROMPT + "\n\n" + project_context

    return Agent(
        model=_models.get_qa_model(),
        system_prompt=full_prompt,
        tools=[file_read, file_write, editor, http_request],
        callback_handler=callback_handler,
    )


@tool
def qa_engineer(query: str) -> str:
    """Route testing and quality assurance tasks to the QA specialist."""
    try:
        agent = create_qa_agent()
        response = agent(query)
        return str(response)
    except Exception as e:
        return f"Error in QA agent: {e}"
