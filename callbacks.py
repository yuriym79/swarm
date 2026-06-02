"""Custom callback handlers for agent observability.

These handlers let you see exactly what agents are doing in the CLI:
- Which tools they call (file_read, editor, http_request)
- What files/URLs they access
- What text they generate
- Event loop lifecycle (start, tool use, completion)

Usage:
    from callbacks import verbose_handler, minimal_handler

    agent = Agent(
        model=...,
        system_prompt=...,
        tools=[...],
        callback_handler=verbose_handler,  # or minimal_handler
    )
"""

import json
from datetime import datetime


def verbose_handler(**kwargs):
    """Full visibility into agent activity — shows tools, files, and output.

    Prints:
    - 🔄 Event loop lifecycle (init, start, complete)
    - 🔧 Tool calls with their arguments
    - 📄 Files being read/written
    - 📡 HTTP requests being made
    - 📝 Generated text (streaming)
    """
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Event loop lifecycle
    if kwargs.get("init_event_loop", False):
        print(f"\n{'═' * 70}")
        print(f"  [{timestamp}] 🔄 Agent event loop initialized")
        print(f"{'═' * 70}")

    elif kwargs.get("start_event_loop", False):
        print(f"  [{timestamp}] ▶️  New reasoning cycle starting...")

    elif "result" in kwargs:
        print(f"\n  [{timestamp}] ✅ Agent completed")
        print(f"{'═' * 70}\n")

    elif kwargs.get("force_stop", False):
        reason = kwargs.get("force_stop_reason", "unknown")
        print(f"\n  [{timestamp}] 🛑 Agent force-stopped: {reason}")

    # Tool usage — the most important visibility
    if "current_tool_use" in kwargs:
        tool_use = kwargs["current_tool_use"]
        tool_name = tool_use.get("name", "")

        if tool_name:
            input_data = tool_use.get("input", {})

            # Format based on tool type
            if tool_name == "file_read":
                path = input_data.get("path", "unknown")
                print(f"  [{timestamp}] 📄 READ: {path}")

            elif tool_name == "file_write":
                path = input_data.get("path", "unknown")
                content_len = len(input_data.get("content", ""))
                print(f"  [{timestamp}] ✏️  WRITE: {path} ({content_len} chars)")

            elif tool_name == "editor":
                command = input_data.get("command", "unknown")
                path = input_data.get("path", "unknown")
                print(f"  [{timestamp}] 📝 EDIT [{command}]: {path}")

            elif tool_name == "http_request":
                method = input_data.get("method", "GET")
                url = input_data.get("url", "unknown")
                print(f"  [{timestamp}] 📡 HTTP {method}: {url}")

            else:
                # Generic tool call
                args_summary = ", ".join(
                    f"{k}={repr(v)[:50]}" for k, v in input_data.items()
                )
                print(f"  [{timestamp}] 🔧 TOOL [{tool_name}]: {args_summary[:100]}")

    # Text output (streaming)
    if "data" in kwargs:
        print(kwargs["data"], end="", flush=True)


def minimal_handler(**kwargs):
    """Compact handler — shows only tool calls and final output.

    Good for when you want to see what context the agent reads without
    cluttering the terminal with full response text.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Tool usage only
    if "current_tool_use" in kwargs:
        tool_use = kwargs["current_tool_use"]
        tool_name = tool_use.get("name", "")
        input_data = tool_use.get("input", {})

        if tool_name == "file_read":
            print(f"  [{timestamp}] 📄 {input_data.get('path', '?')}")
        elif tool_name == "file_write":
            print(f"  [{timestamp}] ✏️  {input_data.get('path', '?')}")
        elif tool_name == "editor":
            print(f"  [{timestamp}] 📝 {input_data.get('command', '?')}: {input_data.get('path', '?')}")
        elif tool_name == "http_request":
            print(f"  [{timestamp}] 📡 {input_data.get('method', 'GET')} {input_data.get('url', '?')}")
        elif tool_name:
            print(f"  [{timestamp}] 🔧 {tool_name}")

    # Only print the final result, not streaming text
    if "result" in kwargs:
        print(f"\n  [{timestamp}] ✅ Done\n")


def silent_handler(**kwargs):
    """No output — captures everything silently.

    Useful when using an agent as a tool inside the orchestrator
    where you don't want nested output.
    """
    pass
