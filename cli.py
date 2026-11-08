#!/usr/bin/env python3
"""
OSINT Suite – unified CLI
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@click.group()
def cli():
    """Multifunctional free OSINT toolkit"""
    pass


@cli.command()
@click.argument("username")
def username(username: str):
    """Search username across social networks (Sherlock)"""
    console.print(Panel(f"[bold blue]Searching username:[/] {username}", title="Sherlock"))

    from core.username_search import search_username
    results = search_username(username)

    table = Table(title=f"Results for '{username}'")
    table.add_column("Site", style="cyan")
    table.add_column("URL", style="green")
    table.add_column("Exists", style="magenta")

    found = 0
    for r in results:
        exists = r.get("exists", False)
        if exists:
            found += 1
        table.add_row(
            str(r.get("site", "")),
            str(r.get("url", "")),
            "Yes" if exists else "No",
        )

    console.print(table)
    console.print(f"\n[bold green]Found on {found} sites[/]")


@cli.command()
@click.argument("phone")
@click.option("--vk", is_flag=True, help="Also show VK search guidance")
def phone(phone: str, vk: bool):
    """Lookup phone number (free operator/region + optional VK guidance)"""
    console.print(Panel(f"[bold blue]Phone lookup:[/] {phone}", title="Phone"))

    from core.phone_lookup import lookup_phone
    result = lookup_phone(phone)

    table = Table(show_header=False)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Input", result.get("input", ""))
    table.add_row("Normalized", result.get("normalized", ""))
    table.add_row("Country", str(result.get("country")))
    table.add_row("Operator", str(result.get("operator")))
    table.add_row("Region", str(result.get("region")))
    console.print(table)
    console.print(f"[dim]{result.get('notes')}[/]")

    if vk:
        from core.vk_osint import search_vk_by_phone, format_vk_result
        vk_data = search_vk_by_phone(phone)
        console.print(Panel(format_vk_result(vk_data), title="VK OSINT"))


@cli.command()
@click.argument("url")
def contacts(url: str):
    """Extract emails, phones and social links from a webpage"""
    console.print(Panel(f"[bold blue]Scraping contacts from:[/] {url}", title="Contacts"))

    from core.contact_scraper import scrape_contacts
    result = scrape_contacts(url)

    if result.get("error"):
        console.print(f"[red]Error:[/] {result['error']}")
        return

    table = Table(title="Found contacts")
    table.add_column("Type", style="cyan")
    table.add_column("Value", style="green")

    for e in result.get("emails") or []:
        table.add_row("email", e)
    for p in result.get("phones") or []:
        table.add_row("phone", p)
    for net, urls in (result.get("social") or {}).items():
        for u in urls:
            table.add_row(net, u)

    if table.row_count == 0:
        console.print("[yellow]Nothing found.[/]")
    else:
        console.print(table)


@cli.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option("--db", "database_folder", default=".", help="Folder with images to search against")
@click.option("--threshold", default=10, help="Max perceptual hash distance (lower = stricter)")
def image(image_path: str, database_folder: str, threshold: int):
    """Reverse image / perceptual hash search (local, free)"""
    console.print(Panel(f"[bold blue]Image search:[/] {image_path}", title="Perceptual Hash"))

    from core.reverse_image import phash_search
    matches = phash_search(image_path, database_folder, threshold=threshold)

    if not matches:
        console.print("[yellow]No similar images found in the database folder.[/]")
        console.print("Tip: put reference images in a folder and pass --db path/to/folder")
        return

    table = Table(title="Similar images")
    table.add_column("Distance", style="cyan")
    table.add_column("Path", style="green")

    for path, dist in matches:
        table.add_row(str(dist), path)

    console.print(table)


@cli.command()
@click.argument("query")
@click.option("--region", default=None, help="Region / court (optional)")
@click.option("--year", default=None, type=int, help="Year (optional)")
def court(query: str, region: str, year: int):
    """Russian courts search interface (sudrf guidance)"""
    console.print(Panel(f"[bold blue]Court search:[/] {query}", title="Sudrf"))

    from core.court_search import search_cases, format_court_result
    data = search_cases(query=query, region=region, year=year)
    console.print(Panel(format_court_result(data), title="Result"))

    if data.get("suggested_urls"):
        console.print("[bold]Suggested official sources:[/]")
        for u in data["suggested_urls"]:
            console.print(f"  • {u}")


@cli.command()
@click.option("--username", default=None)
@click.option("--phone", default=None)
@click.option("--url", default=None, help="Page URL for contact scraping")
@click.option("--image", "image_path", default=None, type=click.Path(exists=True))
@click.option("--output", default="report.md")
@click.option("--json-output", default=None, help="Also write machine-readable JSON")
def report(username, phone, url, image_path, output, json_output):
    """Generate full OSINT report (Markdown + optional JSON)"""
    console.print("[bold green]Generating report...[/]")

    username_data = None
    phone_data = None
    contacts_data = None
    image_data = None

    if username:
        from core.username_search import search_username
        results = search_username(username)
        found = [r for r in results if r.get("exists")]
        username_data = {
            "query": username,
            "found": found,
            "total_checked": len(results),
        }

    if phone:
        from core.phone_lookup import lookup_phone
        from core.vk_osint import search_vk_by_phone
        phone_data = {
            "lookup": lookup_phone(phone),
            "vk": search_vk_by_phone(phone),
        }

    if url:
        from core.contact_scraper import scrape_contacts
        contacts_data = scrape_contacts(url)

    if image_path:
        image_data = {"path": image_path}

    from core.report import build_report, save_report
    data = build_report(
        username_data=username_data,
        phone_data=phone_data,
        contacts_data=contacts_data,
        image_data=image_data,
    )
    written = save_report(data, md_path=output, json_path=json_output)

    console.print(f"[green]Markdown → {written['markdown']}[/]")
    if "json" in written:
        console.print(f"[green]JSON → {written['json']}[/]")


if __name__ == "__main__":
    cli()
