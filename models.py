"""Model configurations for each agent role.

Strategy:
- Code-intensive agents (frontend, backend, QA, devops) → Local Ollama (qwen3-coder:30b)
  Saves Bedrock costs while handling code generation well.
- Reasoning-heavy agents (architect, security, orchestrator) → Bedrock (Claude)
  These need deep reasoning and complex analysis that benefits from larger models.
- Technical writer → Bedrock (Claude Sonnet)
  Good prose requires a strong language model.

Prerequisites:
- Ollama running locally: ollama serve
- Model pulled: ollama pull qwen3-coder:30b
- AWS credentials configured for Bedrock agents
"""

from strands.models import BedrockModel
from strands.models.ollama import OllamaModel

# Model constants
SONNET_MODEL = "us.anthropic.claude-sonnet-4-6"
OPUS_MODEL = "us.anthropic.claude-opus-4-7"
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_CODE_MODEL = "qwen3-coder:30b"


# ─── Bedrock models (reasoning-heavy tasks) ───────────────────────────────────

def get_orchestrator_model() -> BedrockModel:
    """Claude Sonnet for fast routing decisions across agents."""
    return BedrockModel(
        model_id=SONNET_MODEL,
        temperature=0.2,
    )


def get_architect_model() -> BedrockModel:
    """Claude Opus for deep system design and architecture reasoning."""
    return BedrockModel(
        model_id=OPUS_MODEL,
        temperature=0.3,
    )


def get_security_model() -> BedrockModel:
    """Claude Opus for thorough threat analysis and security review."""
    return BedrockModel(
        model_id=OPUS_MODEL,
        temperature=0.1,
    )


def get_writer_model() -> BedrockModel:
    """Claude Sonnet for clear, well-structured documentation."""
    return BedrockModel(
        model_id=SONNET_MODEL,
        temperature=0.4,
    )


# ─── Ollama models (code-intensive tasks) ─────────────────────────────────────

def get_frontend_model() -> OllamaModel:
    """Local qwen3-coder for React/Next.js UI code generation."""
    return OllamaModel(
        host=OLLAMA_HOST,
        model_id=OLLAMA_CODE_MODEL,
    )


def get_backend_model() -> OllamaModel:
    """Local qwen3-coder for API and backend code generation."""
    return OllamaModel(
        host=OLLAMA_HOST,
        model_id=OLLAMA_CODE_MODEL,
    )


def get_qa_model() -> OllamaModel:
    """Local qwen3-coder for test code generation."""
    return OllamaModel(
        host=OLLAMA_HOST,
        model_id=OLLAMA_CODE_MODEL,
    )


def get_devops_model() -> OllamaModel:
    """Local qwen3-coder for Dockerfiles, CI/CD, and infra configs."""
    return OllamaModel(
        host=OLLAMA_HOST,
        model_id=OLLAMA_CODE_MODEL,
    )
