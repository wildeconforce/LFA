"""Example: end-to-end synthetic case demo (skeleton).

This script will, when modules are implemented:
    1. Load synthetic plaintiff + defendant personas from Nemotron.
    2. Generate a fictional 약정금+공갈 case with asymmetric evidence.
    3. Run the analysis pipeline (Modules 1-8).
    4. Produce a draft preparatory brief.
    5. Run the mock trial simulator (Modules 9-13).
    6. Print outcome distribution across judge personas.

Currently a skeleton — none of the modules are implemented yet. This
file documents the *intended* end-to-end flow.

Run:
    python -m examples.synthetic_case_demo
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

from lfa import DISCLAIMER

console = Console()


def main() -> None:
    console.print(Panel.fit(
        "LFA Synthetic Case Demo (skeleton)\n"
        "Modules are not yet implemented.\n"
        "This script documents the intended pipeline.",
        title="lfa demo",
        border_style="yellow",
    ))

    steps = [
        ("Load personas",
         "load_personas(role='party', count=2, ...)"),
        ("Generate case",
         "generate_case(CaseGenerationConfig(issue_keywords=['약정금','공갈'],"
         " asymmetry_bias=0.6, ...))"),
        ("Scan case",
         "scan_case(case_dir)"),
        ("Detect timeline conflicts",
         "detect_conflicts(case)"),
        ("Find weaknesses",
         "break_logic(case, target_party='plaintiff')"),
        ("Hunt verified precedents",
         "hunt_precedents(['강박에 의한 의사표시'])"),
        ("Write draft brief",
         "write_document(case, kind='preparatory_brief', tone='hybrid', ...)"),
        ("Verify facts",
         "verify_draft(draft, case)"),
        ("Red-team draft",
         "red_team(draft, case)"),
        ("Run mock trial arena",
         "run_arena(case, plaintiff_counsel, defendant_counsel, ...)"),
        ("Adjudicate by judge persona",
         "adjudicate(transcript, judge)"),
        ("Aggregate outcomes",
         "analyze_outcomes(rulings)"),
    ]

    for i, (name, call) in enumerate(steps, start=1):
        console.print(f"[bold cyan]{i:2d}.[/bold cyan] {name}")
        console.print(f"     [dim]{call}[/dim]")

    console.print()
    console.print(Panel(DISCLAIMER, title="Disclaimer", border_style="red"))


if __name__ == "__main__":
    main()
