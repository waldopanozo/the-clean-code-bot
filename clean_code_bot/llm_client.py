"""Cliente LLM: Groq (OpenAI-compatible) u OpenAI."""

from __future__ import annotations

import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

Provider = Literal["groq", "openai"]


def _resolve_provider(explicit: str | None) -> Provider:
    if explicit in ("groq", "openai"):
        return explicit  # type: ignore[return-value]
    env = (os.environ.get("LLM_PROVIDER") or "").strip().lower()
    if env in ("groq", "openai"):
        return env  # type: ignore[return-value]
    if os.environ.get("GROQ_API_KEY"):
        return "groq"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    raise RuntimeError(
        "Definí GROQ_API_KEY o OPENAI_API_KEY (y opcionalmente LLM_PROVIDER=groq|openai) en .env"
    )


def _resolve_model(provider: Provider, explicit: str | None) -> str:
    if explicit:
        return explicit
    default = os.environ.get("LLM_MODEL")
    if default:
        return default
    if provider == "groq":
        return "llama-3.3-70b-versatile"
    return "gpt-4o-mini"


def get_client(provider: Provider) -> tuple[OpenAI, str]:
    if provider == "groq":
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            raise RuntimeError("GROQ_API_KEY no definida")
        client = OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")
        return client, "https://api.groq.com/openai/v1"
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY no definida")
    client = OpenAI(api_key=key)
    return client, "https://api.openai.com/v1"


def complete_chat(
    *,
    system_prompt: str,
    user_message: str,
    provider: str | None = None,
    model: str | None = None,
) -> str:
    pv = _resolve_provider(provider)
    client, _ = get_client(pv)
    md = _resolve_model(pv, model)
    resp = client.chat.completions.create(
        model=md,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )
    choice = resp.choices[0].message.content
    if not choice:
        raise RuntimeError("El modelo devolvió contenido vacío.")
    return choice
