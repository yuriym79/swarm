"""CLI entry point for the dev swarm orchestrator.

Usage:
    python -m swarm "Design the database schema for a user system"
    python -m swarm "Build a responsive navigation component"
    python -m swarm --agent architect "What tech stack should we use?"
    python -m swarm --agent frontend "Build a ProductCard component"
"""

import argparse
import sys
from pathlib import Path

# Add swarm root to path for dynamic imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.agent import create_orchestrator, _load_agent_tool


AVAILABLE_AGENTS = {
    "orchestrator": None,  # Special case — uses all agents
    "architect": ("architect", "architect"),
    "frontend": ("front-end-engineer", "frontend_engineer"),
    "backend": ("software-engineer", "backend_engineer"),
    "qa": ("qa-engineer", "qa_engineer"),
    "devops": ("devops-engineer", "devops_engineer"),
    "security": ("security-engineer", "security_engineer"),
    "writer": ("technical-writer", "technical_writer"),
}


def main():
    parser = argparse.ArgumentParser(
        description="Dev Swarm — Multi-agent software development system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m swarm "Build the user authentication API"
  python -m swarm --agent architect "Design the database schema"
  python -m swarm --agent frontend "Build a responsive card component"
  python -m swarm --list-agents
        """,
    )
    parser.add_argument("task", nargs="?", help="The task to execute")
    parser.add_argument(
        "--agent", "-a",
        choices=list(AVAILABLE_AGENTS.keys()),
        default="orchestrator",
        help="Route directly to a specific agent (default: orchestrator)",
    )
    parser.add_argument(
        "--list-agents",
        action="store_true",
        help="List all available agents",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all agent activity (tool calls, files read, HTTP requests)",
    )
    parser.add_argument(
        "--minimal", "-m",
        action="store_true",
        help="Show only tool calls (compact observability)",
    )

    args = parser.parse_args()

    if args.list_agents:
        print("\n🐝 Dev Swarm — Available Agents\n")
        print(f"  {'Agent':<14} {'Directory':<22} Description")
        print(f"  {'─' * 14} {'─' * 22} {'─' * 40}")
        print(f"  {'orchestrator':<14} {'orchestrator/':<22} Routes tasks to specialists")
        print(f"  {'architect':<14} {'architect/':<22} System design & tech decisions")
        print(f"  {'frontend':<14} {'front-end-engineer/':<22} React/Next.js UI development")
        print(f"  {'backend':<14} {'software-engineer/':<22} API endpoints & business logic")
        print(f"  {'qa':<14} {'qa-engineer/':<22} Testing & quality assurance")
        print(f"  {'devops':<14} {'devops-engineer/':<22} Deployment & infrastructure")
        print(f"  {'security':<14} {'security-engineer/':<22} Auth & security hardening")
        print(f"  {'writer':<14} {'technical-writer/':<22} Documentation & guides")
        print()
        return

    if not args.task:
        parser.print_help()
        return

    print(f"\n🐝 Dev Swarm — Routing to: {args.agent}\n")
    print(f"📋 Task: {args.task}\n")
    print("─" * 60)

    # Load callback handler based on flags
    from pathlib import Path as P2
    import importlib.util as ilu
    cb_path = P2(__file__).parent / "callbacks.py"
    cb_spec = ilu.spec_from_file_location("callbacks", cb_path)
    cb_mod = ilu.module_from_spec(cb_spec)
    cb_spec.loader.exec_module(cb_mod)

    if args.verbose:
        callback = cb_mod.verbose_handler
    elif args.minimal:
        callback = cb_mod.minimal_handler
    else:
        callback = None  # Default streaming output

    if args.agent == "orchestrator":
        agent = create_orchestrator()
    else:
        directory, tool_name = AVAILABLE_AGENTS[args.agent]
        # For direct agent usage, we create the agent directly (not as a tool)
        import importlib.util

        agent_module_path = Path(__file__).parent / directory / "agent.py"
        spec = importlib.util.spec_from_file_location("direct_agent", agent_module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Each agent module has a create_*_agent() function
        create_fn_name = [
            name for name in dir(module) if name.startswith("create_") and name.endswith("_agent")
        ][0]
        create_fn = getattr(module, create_fn_name)

        # Try to pass callback_handler if the function supports it
        import inspect
        sig = inspect.signature(create_fn)
        if "callback_handler" in sig.parameters:
            agent = create_fn(callback_handler=callback)
        else:
            agent = create_fn()

    # Run the agent
    response = agent(args.task)
    print("\n" + "─" * 60)
    print("\n✅ Done\n")


if __name__ == "__main__":
    main()
