"""Orchestrator agent — routes tasks to specialist agents."""

import importlib.util
import sys
from pathlib import Path

from strands import Agent

# Load prompts from same directory
_prompts_path = Path(__file__).parent / "prompts.py"
_spec = importlib.util.spec_from_file_location("orchestrator_prompts", _prompts_path)
_prompts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_prompts)
ORCHESTRATOR_SYSTEM_PROMPT = _prompts.ORCHESTRATOR_SYSTEM_PROMPT

# Load model config
_models_path = Path(__file__).parent.parent / "models.py"
_mspec = importlib.util.spec_from_file_location("swarm_models", _models_path)
_models = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(_models)

# The agent directories use hyphens (front-end-engineer), which aren't valid
# Python identifiers. We import them dynamically.
SWARM_ROOT = Path(__file__).parent.parent


def _load_agent_tool(directory: str, tool_name: str):
    """Dynamically load a tool function from a hyphenated directory."""
    agent_module_path = SWARM_ROOT / directory / "agent.py"
    spec = importlib.util.spec_from_file_location(
        f"swarm.{directory.replace('-', '_')}.agent", agent_module_path
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return getattr(module, tool_name)


def create_orchestrator() -> Agent:
    """Create the orchestrator agent with Claude Sonnet 4 for fast routing.

    All specialist agents are loaded as tools — the orchestrator decides
    which specialist handles which part of a request.
    """
    tools = [
        _load_agent_tool("architect", "architect"),
        _load_agent_tool("front-end-engineer", "frontend_engineer"),
        _load_agent_tool("software-engineer", "backend_engineer"),
        _load_agent_tool("qa-engineer", "qa_engineer"),
        _load_agent_tool("devops-engineer", "devops_engineer"),
        _load_agent_tool("security-engineer", "security_engineer"),
        _load_agent_tool("technical-writer", "technical_writer"),
    ]

    return Agent(
        model=_models.get_orchestrator_model(),
        system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
        tools=tools,
    )
