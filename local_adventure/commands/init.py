import os
import click
import shutil

@click.command(context_settings={"max_content_width": 220})
def init():
    base_dir = os.path.expanduser(os.getenv("LA_ROOT_DIR", "~/.local_adventure"))

    # Check if the base directory already exists
    if os.path.exists(base_dir):
        confirmation = input(f"❓ Directory {base_dir} already exists.\n❓ Do you want to delete and recreate it? (yes/no): ").strip().lower()
        if confirmation != "yes":
            print("❌ Initialization aborted.")
            return
        shutil.rmtree(base_dir)
        print(f"🟢 Deleted existing directory: {base_dir}")

    # Define the directory structure without `tx` directories
    structure = [
        "primary/cx",
        "secondary/cx",
        "tertiary/cx",
    ]

    # Create the directories
    for path in structure:
        full_path = os.path.join(base_dir, path)
        os.makedirs(full_path, exist_ok=True)
        print(f"🟢 Created: {full_path}")

    print("🟢 Initialization complete.")