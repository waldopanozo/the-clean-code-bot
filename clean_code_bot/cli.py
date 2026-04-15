"""CLI con Click: refactor y opciones."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from clean_code_bot.refactorer import refactor_file


@click.group()
@click.version_option(version="0.1.0", prog_name="clean-code-bot")
def cli() -> None:
    """The Clean Code Bot: refactorizador con CoT y saneamiento de entrada."""
    pass


@cli.command("refactor")
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
    help="Archivo de salida. Si se omite, se imprime en stdout.",
)
@click.option("--provider", type=click.Choice(["groq", "openai"]), default=None)
@click.option("--model", type=str, default=None, help="Modelo (sobreescribe LLM_MODEL)")
@click.option(
    "--dry-run",
    is_flag=True,
    help="Imprime la respuesta completa del modelo (CoT + código) sin extraer solo el código.",
)
def refactor_cmd(
    input_file: Path,
    output: Path | None,
    provider: str | None,
    model: str | None,
    dry_run: bool,
) -> None:
    """Refactoriza INPUT_FILE y escribe el resultado en --output o stdout."""
    try:
        result = refactor_file(
            input_file,
            provider=provider,
            model=model,
            dry_run=dry_run,
        )
    except Exception as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        sys.exit(1)

    if output:
        output.write_text(result, encoding="utf-8")
        click.echo(click.style(f"Escrito: {output}", fg="green"))
    else:
        click.echo(result)


if __name__ == "__main__":
    cli()
