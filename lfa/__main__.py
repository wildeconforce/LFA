"""LFA CLI entry point (skeleton)."""

import typer
from rich.console import Console

from lfa import __version__, DISCLAIMER

app = typer.Typer(
    name="lfa",
    help="Legal Framework Analysis — modular Korean legal case analyzer.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def version():
    """Print LFA version."""
    console.print(f"LFA v{__version__}")


@app.command()
def scan(case_dir: str):
    """Scan a case directory and produce a structured fact extract.

    Module 1 — CASE_SCANNER. Skeleton: not yet functional.
    """
    console.print(f"[yellow]CASE_SCANNER skeleton — would scan {case_dir}[/yellow]")
    console.print(f"[dim]{DISCLAIMER}[/dim]")


@app.command()
def break_logic(case_file: str):
    """Detect logical/temporal/evidentiary weaknesses in opposing claims.

    Module 2 — LOGIC_BREAKER. Skeleton: not yet functional.
    """
    console.print(f"[yellow]LOGIC_BREAKER skeleton — would analyze {case_file}[/yellow]")
    console.print(f"[dim]{DISCLAIMER}[/dim]")


@app.command()
def hunt(query: str):
    """Search and cross-verify Korean Supreme Court precedents.

    Module 3 — PRECEDENT_HUNTER. Skeleton: not yet functional.
    """
    console.print(f"[yellow]PRECEDENT_HUNTER skeleton — would search '{query}'[/yellow]")
    console.print(f"[dim]{DISCLAIMER}[/dim]")


@app.command()
def write(case_file: str, kind: str = "brief"):
    """Generate a brief/answer/demand-letter draft.

    Module 4 — DOC_WRITER. Skeleton: not yet functional.
    """
    console.print(f"[yellow]DOC_WRITER skeleton — would draft {kind} from {case_file}[/yellow]")
    console.print(f"[dim]{DISCLAIMER}[/dim]")


@app.command()
def simulate(seed: int = 42):
    """Run a Mock Trial simulation with synthetic personas.

    Modules 9–13 — Mock Trial Engine. Skeleton: not yet functional.
    """
    console.print(f"[yellow]MOCK_TRIAL skeleton — would simulate with seed={seed}[/yellow]")
    console.print(f"[dim]{DISCLAIMER}[/dim]")


if __name__ == "__main__":
    app()
