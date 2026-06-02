"""Project context loader for swarm agents.

Provides agents with actual project structure, file paths, API response formats,
and database schema so they don't guess or hallucinate imports.

Usage in agent prompts:
    from context import get_project_context
    prompt = SYSTEM_PROMPT + "\n\n" + get_project_context("/path/to/project")
"""

import os
from pathlib import Path


def get_project_context(project_root: str) -> str:
    """Generate a context string describing the actual project structure."""
    root = Path(project_root)

    context_parts = [
        "## CURRENT PROJECT CONTEXT",
        "",
        "You are working on a real project. Use ONLY these actual paths and imports.",
        "Do NOT invent imports or file paths that don't exist.",
        "",
    ]

    # File structure
    context_parts.append("### Project Structure")
    context_parts.append("```")
    for path in _walk_project(root, max_depth=4):
        context_parts.append(path)
    context_parts.append("```")
    context_parts.append("")

    # API response format
    context_parts.append("### API Response Format (ALWAYS use this)")
    context_parts.append("```typescript")
    context_parts.append('// Success: { status: "success", data: T }')
    context_parts.append('// Error: { status: "error", error: { message: string, field?: string } }')
    context_parts.append('// Paginated: { status: "success", data: T[], pagination: { page, limit, total, totalPages } }')
    context_parts.append("")
    context_parts.append("// Frontend must access: json.data (NOT json directly)")
    context_parts.append("// Example: const json = await res.json(); setProducts(json.data);")
    context_parts.append("```")
    context_parts.append("")

    # Valid imports for backend
    context_parts.append("### Valid Backend Imports")
    context_parts.append("```typescript")
    context_parts.append('import { prisma } from "../lib/prisma";  // Prisma client singleton')
    context_parts.append('import { validate } from "../middleware/validate";  // Zod validation middleware')
    context_parts.append('import { requireAuth } from "../middleware/auth";  // JWT auth middleware')
    context_parts.append('import { AppError, NotFoundError, ValidationError } from "../lib/errors";')
    context_parts.append('import { createProductSchema, productQuerySchema, ... } from "@headstash/shared";')
    context_parts.append("```")
    context_parts.append("")

    # Valid imports for frontend
    context_parts.append("### Valid Frontend Imports")
    context_parts.append("```typescript")
    context_parts.append('import { useCart } from "@/lib/cart";  // Zustand cart store')
    context_parts.append('import { apiFetch } from "@/lib/api";  // Typed fetch wrapper')
    context_parts.append('import { Header } from "@/components/storefront/Header";')
    context_parts.append('import { Hero } from "@/components/storefront/Hero";')
    context_parts.append('import { Footer } from "@/components/storefront/Footer";')
    context_parts.append('import { CartDrawer } from "@/components/storefront/CartDrawer";')
    context_parts.append('import ProductCard from "@/components/storefront/ProductCard";')
    context_parts.append('import FilterTabs from "@/components/storefront/FilterTabs";')
    context_parts.append('// @/ maps to apps/web/ (NOT apps/web/src/)')
    context_parts.append('// Do NOT import from @/types/* (does not exist)')
    context_parts.append("```")
    context_parts.append("")

    # Prisma models
    context_parts.append("### Prisma Models (use exact names)")
    context_parts.append("```")
    context_parts.append("prisma.product         - Product catalog")
    context_parts.append("prisma.productImage    - Product images")
    context_parts.append("prisma.order           - Customer orders")
    context_parts.append("prisma.orderLineItem   - Order line items")
    context_parts.append("prisma.orderStatusLog  - Order status history")
    context_parts.append("prisma.adminUser       - Admin accounts (NOT prisma.user)")
    context_parts.append("prisma.promoCode       - Discount codes")
    context_parts.append("prisma.affiliate       - Affiliate partners")
    context_parts.append("prisma.waitlistEntry   - Email waitlist")
    context_parts.append("prisma.smartCard       - NFC smart cards")
    context_parts.append("prisma.loginAttempt    - Login rate limiting")
    context_parts.append("```")
    context_parts.append("")

    # Tailwind brand classes
    context_parts.append("### Tailwind Brand Classes")
    context_parts.append("```")
    context_parts.append("Backgrounds: bg-bg (main dark), bg-bg-2 (panels), bg-bg-3 (hover)")
    context_parts.append("Text: text-ink (primary), text-ink-dim (secondary)")
    context_parts.append("Accents: text-gold, bg-gold, border-gold-soft, text-purple, bg-purple")
    context_parts.append("Borders: border-grey-line")
    context_parts.append("Fonts: font-display (Cinzel), font-serif (Cormorant), font-sans (Jost)")
    context_parts.append("Breakpoint: desktop: (>=860px), mobile: (<860px)")
    context_parts.append("```")
    context_parts.append("")

    # File write instructions
    context_parts.append("### CRITICAL: File Writing Rules")
    context_parts.append("- Write EXACTLY ONE file per request")
    context_parts.append("- Use the FULL absolute path provided in the task")
    context_parts.append("- Do NOT create additional helper files unless explicitly asked")
    context_parts.append("- Do NOT import from paths that don't exist in the project structure above")
    context_parts.append("- Always use 'use client' directive for components with hooks or browser APIs")

    return "\n".join(context_parts)


def _walk_project(root: Path, max_depth: int = 4, prefix: str = "") -> list[str]:
    """Walk project tree, excluding node_modules, .next, dist, .git."""
    results = []
    exclude = {"node_modules", ".next", "dist", ".git", "__pycache__", ".venv", ".turbo"}

    if not root.exists():
        return results

    try:
        entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name))
    except PermissionError:
        return results

    for entry in entries:
        if entry.name in exclude:
            continue
        if entry.name.startswith(".") and entry.name not in (".env.example", ".gitignore"):
            continue

        rel = str(entry.relative_to(root.parent.parent.parent))  # relative to project root
        if entry.is_dir():
            results.append(f"{prefix}{entry.name}/")
            if max_depth > 0:
                results.extend(_walk_project(entry, max_depth - 1, prefix + "  "))
        else:
            results.append(f"{prefix}{entry.name}")

    return results
