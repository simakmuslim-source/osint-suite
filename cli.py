#!/usr/bin/env python3
"""
OSINT Suite – unified CLI
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
def cli():
    """Multifunctional free OSINT toolkit"""
    pass

@cli.command()
@click.argument("username")
def username(username: str):
    """Search username across social networks (Sherlock wrapper)"""
    console.print(f"[bold blue]Searching username:[/] {username}")
    console.print("[yellow]TODO: integrate Sherlock[/]")
    # from core.username_search import search_username
    # results = search_username(username)
    # ...

@cli.command()
@click.argument("phone")
def phone(phone: str):
    """Lookup phone number (Gokboru + vkOsint)"""
    console.print(f"[bold blue]Phone lookup:[/] {phone}")
    console.print("[yellow]TODO: integrate phone modules[/]")

@cli.command()
@click.argument("image_path", type=click.Path(exists=True))
def image(image_path: str):
    """Reverse image / perceptual hash search"""
    console.print(f"[bold blue]Image search:[/] {image_path}")
    console.print("[yellow]TODO: integrate image-match / perceptual hash[/]")

@cli.command()
@click.option("--username", default=None)
@click.option("--phone", default=None)
@click.option("--image", "image_path", default=None, type=click.Path(exists=True))
@click.option("--output", default="report.md")
def report(username, phone, image_path, output):
    """Generate full OSINT report"""
    console.print("[bold green]Generating report...[/]")
    lines = ["# OSINT Report\n"]
    if username:
        lines.append(f"## Username: `{username}`\n")
        lines.append("- (Sherlock results will appear here)\n")
    if phone:
        lines.append(f"## Phone: `{phone}`\n")
        lines.append("- (Phone lookup results will appear here)\n")
    if image_path:
        lines.append(f"## Image: `{image_path}`\n")
        lines.append("- (Reverse image results will appear here)\n")
    Path(output).write_text("\n".join(lines), encoding="utf-8")
    console.print(f"[green]Report saved to {output}[/]")

if __name__ == "__main__":
    cli()
