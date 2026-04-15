"""Orquestación: leer archivo, saneamiento, LLM, extracción del bloque de código."""

from __future__ import annotations

import re
from pathlib import Path

from clean_code_bot.llm_client import complete_chat
from clean_code_bot.prompt_templates import COT_SYSTEM_PROMPT, build_user_message
from clean_code_bot.sanitizer import read_and_validate_text, wrap_for_llm_user_message


def _language_hint(path: Path) -> str:
    suf = path.suffix.lower()
    if suf in (".js", ".mjs", ".cjs"):
        return "javascript"
    if suf in (".ts", ".tsx"):
        return "typescript"
    return "python"


def _extract_code_fence(full_response: str, fence: str) -> str | None:
    """
    Extrae el primer bloque ```fence ... ``` del texto del modelo.
    """
    pattern = re.compile(
        rf"```{re.escape(fence)}\s*\n(.*?)```",
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(full_response)
    return m.group(1).strip() if m else None


def _pick_fence(path: Path) -> str:
    suf = path.suffix.lower()
    if suf in (".ts", ".tsx"):
        return "typescript"
    if suf in (".js", ".jsx", ".mjs", ".cjs"):
        return "javascript"
    return "python"


def refactor_file(
    path: Path,
    *,
    provider: str | None = None,
    model: str | None = None,
    dry_run: bool = False,
) -> str:
    source = read_and_validate_text(path)
    hint = _language_hint(path)
    user = build_user_message(wrap_for_llm_user_message(source, hint))
    raw = complete_chat(
        system_prompt=COT_SYSTEM_PROMPT,
        user_message=user,
        provider=provider,
        model=model,
    )
    if dry_run:
        return raw

    fence = _pick_fence(path)
    code = _extract_code_fence(raw, fence)
    if code is None:
        # fallback: intentar python si el modelo usó otro cercado
        code = _extract_code_fence(raw, "python") or _extract_code_fence(raw, "py")
    if code is None:
        raise RuntimeError(
            "No se encontró un bloque de código cercado en la respuesta del modelo. "
            "Revisá la salida completa o repetí con --dry-run."
        )
    return code
