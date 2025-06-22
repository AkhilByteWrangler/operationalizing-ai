#!/usr/bin/env python

import click
from rich import print
from q_engine import ask_q
import memory

@click.group(invoke_without_command=True)
@click.argument("query", required=False)
@click.pass_context
def cli(ctx, query):
    """Amazon Q-style CLI Assistant"""
    if query:
        print("[bold green]Amazon Q is thinking...[/bold green]")
        response = ask_q(query)
        print(f"\n[white on blue]Q:[/white on blue] {response}")
    elif ctx.invoked_subcommand is None:
        print("[bold cyan]🧠 Welcome to Amazon Q CLI (type 'exit' or 'quit' to end)[/bold cyan]\n")
        while True:
            try:
                user_input = input("You 🧑‍💻: ").strip()
                if user_input.lower() in ("exit", "quit"):
                    print("[bold green]👋 Goodbye![/bold green]")
                    break
                if not user_input:
                    continue
                print("[bold green]Amazon Q is thinking...[/bold green]")
                response = ask_q(user_input)
                print(f"\n[white on blue]Q:[/white on blue] {response}\n")
            except KeyboardInterrupt:
                print("\n[bold red]Interrupted. Exiting...[/bold red]")
                break
            except Exception as e:
                print(f"[bold red]❌ Error:[/bold red] {e}")

@cli.command()
def clear():
    """Clear conversation memory."""
    memory.clear()
    print("[bold yellow]🧠 Memory cleared.[/bold yellow]")

if __name__ == "__main__":
    cli()
