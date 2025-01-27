import click
from .commands import init, dr, tree, cx

@click.group(invoke_without_command=True)
@click.pass_context
def locadv(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Welcome to Local Adventure!")
        click.echo("\nAvailable`` commands:")
        click.echo(ctx.command.get_help(ctx))

locadv.add_command(init)
locadv.add_command(dr)
locadv.add_command(tree)
locadv.add_command(cx)

if __name__ == "__main__":
    locadv()