# Dev Swarm

A reusable multi-agent system built with [Strands Agents](https://strandsagents.com/) for collaborative fullstack software development.

## Architecture

This swarm uses the **Agents-as-Tools** pattern — each specialist agent is wrapped as a callable tool and provided to a central orchestrator. The orchestrator routes tasks to the right specialist based on the work needed.

```
User Request
     │
     ▼
┌─────────────────┐
│  Orchestrator    │  Routes tasks, tracks progress
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼          ▼
┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
│Architect││Frontend││Backend ││  QA    ││ DevOps │
│        ││Engineer││Engineer││Engineer││Engineer│
└────────┘└────────┘└────────┘└────────┘└────────┘
```

## Agents

| Agent | Role |
|-------|------|
| **orchestrator** | Routes tasks, manages handoffs, tracks progress |
| **architect** | Tech stack decisions, system design, database schema |
| **front-end-engineer** | React/Next.js UI, components, styling |
| **software-engineer** | Backend API, business logic, integrations |
| **qa-engineer** | Test plans, test automation, quality gates |
| **devops-engineer** | CI/CD, deployment, infrastructure |
| **security-engineer** | Auth, security headers, vulnerability review |
| **technical-writer** | API docs, README, deployment guides |

## Getting Started

```bash
# Install dependencies
uv sync

# Set up your model provider (e.g., AWS Bedrock, OpenAI)
export AWS_PROFILE=your-profile  # or set OPENAI_API_KEY

# Run the orchestrator
python -m swarm "Design the database schema for a product catalog"

# Run a specific agent directly
python -m swarm --agent architect "What's the best database for this use case?"
python -m swarm --agent frontend "Build a responsive nav component"

# List available agents
python -m swarm --list-agents
```

## Project Structure

```
swarm/
├── orchestrator/          # Central coordinator
│   ├── agent.py           # Orchestrator agent definition
│   └── prompts.py         # System prompt
├── architect/             # System design specialist
│   ├── agent.py
│   └── prompts.py
├── front-end-engineer/    # UI/React specialist
│   ├── agent.py
│   └── prompts.py
├── software-engineer/     # Backend/API specialist
│   ├── agent.py
│   └── prompts.py
├── qa-engineer/           # Testing specialist
│   ├── agent.py
│   └── prompts.py
├── devops-engineer/       # Infrastructure specialist
│   ├── agent.py
│   └── prompts.py
├── security-engineer/     # Security specialist
│   ├── agent.py
│   └── prompts.py
├── technical-writer/      # Documentation specialist
│   ├── agent.py
│   └── prompts.py
└── __main__.py            # CLI entry point
```

## Extending the Swarm

To add a new specialist:
1. Create a directory: `my-agent/`
2. Add `prompts.py` with a system prompt constant
3. Add `agent.py` with a `create_*_agent()` function and a `@tool`-decorated function
4. Register it in `orchestrator/agent.py` and `__main__.py`

## How It Works

Each specialist agent is defined with:
- A **system prompt** describing their expertise and output format
- A set of **tools** they can use (file read/write, shell commands)
- A **@tool decorator** that wraps them as callable functions

The orchestrator receives all specialist tools and uses its system prompt to decide which specialist handles which part of a request. For complex tasks, it can chain multiple specialists together.
