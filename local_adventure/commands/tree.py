import os
import click

@click.command(context_settings={"max_content_width": 220})
def tree():
    def print_tree(base_dir, indent=0):
        for item in sorted(os.listdir(base_dir)):
            path = os.path.join(base_dir, item)
            if os.path.isdir(path):
                print(" " * indent + f"{item}/")
                print_tree(path, indent + 3)
            else:
                print(" " * indent + f"{item}")

    base_dir = os.path.expanduser("~/.local_adventure")
    if os.path.exists(base_dir):
        print("Directory structure:")
        print_tree(base_dir)
    else:
        print("🔴 Base directory does not exist.")