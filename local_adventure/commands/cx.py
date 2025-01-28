import os
import json
import click

BASE_DIR = os.path.expanduser("~/.local_adventure")
CATEGORY_MAP = {
    "1": "primary",
    "2": "secondary",
    "3": "tertiary"
}

def ensure_base_dir():
    for category in CATEGORY_MAP.values():
        os.makedirs(os.path.join(BASE_DIR, category, "cx"), exist_ok=True)

def get_customer_dir(category, name):
    return os.path.join(BASE_DIR, category, "cx", name)

@click.group()
def cx():
    "Manage customer data"
    ensure_base_dir()

@cx.command()
def ls():
    "List all customers"
    customers = []
    for category in CATEGORY_MAP.values():
        cx_dir = os.path.join(BASE_DIR, category, "cx")
        for customer in os.listdir(cx_dir):
            if os.path.isdir(os.path.join(cx_dir, customer)):
                customers.append((category, customer))

    if not customers:
        click.echo("No customers found.")
    else:
        click.echo("Customers:")
        for category, customer in customers:
            click.echo(f"[{category}] {customer}")

@cx.command()
def add():
    "Add a new customer"
    name = click.prompt("Enter customer name", type=str, default="").strip()
    if not name:
        click.echo("Customer name is required.")
        return

    category_choice = click.prompt(
        "Select category: 1 for primary, 2 for secondary, 3 for tertiary", type=str
    ).strip()
    category = CATEGORY_MAP.get(category_choice)
    if not category:
        click.echo("Invalid category selection.")
        return

    zendesk_org = click.prompt("Enter Zendesk organization (optional)", type=str, default="").strip()
    zendesk_link = click.prompt("Enter Zendesk organization link (optional)", type=str, default="").strip()

    customer_dir = get_customer_dir(category, name)
    os.makedirs(customer_dir, exist_ok=True)

    customer_data = {
        "name": name,
        "zendesk_org": zendesk_org,
        "zendesk_link": zendesk_link,
    }

    with open(os.path.join(customer_dir, "customer.json"), "w") as f:
        json.dump(customer_data, f, indent=4)

    click.echo(f"Customer '{name}' added successfully to '{category}'.")

@cx.command()
def open():
    "Open a customer's directory in Visual Studio Code"
    name = click.prompt("Enter customer name to open", type=str).strip()
    for category in CATEGORY_MAP.values():
        customer_dir = get_customer_dir(category, name)
        if os.path.exists(customer_dir):
            os.system(f"code {customer_dir}")
            click.echo(f"Opened directory for customer '{name}' in Visual Studio Code.")
            return

    click.echo(f"Customer '{name}' does not exist.")

@cx.command()
def get():
    "Retrieve a customer's data"
    name = click.prompt("Enter customer name to retrieve", type=str).strip()
    for category in CATEGORY_MAP.values():
        customer_dir = get_customer_dir(category, name)
        try:
            with open(os.path.join(customer_dir, "customer.json"), "r") as f:
                customer_data = json.load(f)
                click.echo(json.dumps(customer_data, indent=4))
                return
        except FileNotFoundError:
            continue

    click.echo(f"Customer '{name}' does not exist.")

@cx.command()
def put():
    "Edit an existing customer's data"
    name = click.prompt("Enter customer name to edit", type=str).strip()
    for category in CATEGORY_MAP.values():
        customer_dir = get_customer_dir(category, name)
        try:
            with open(os.path.join(customer_dir, "customer.json"), "r") as f:
                customer_data = json.load(f)
        except FileNotFoundError:
            continue

        click.echo("Leave fields blank to keep current values.")
        zendesk_org = click.prompt(f"Zendesk organization (current: {customer_data['zendesk_org']})", type=str, default="").strip()
        zendesk_link = click.prompt(f"Zendesk organization link (current: {customer_data['zendesk_link']})", type=str, default="").strip()

        if zendesk_org:
            customer_data['zendesk_org'] = zendesk_org
        if zendesk_link:
            customer_data['zendesk_link'] = zendesk_link

        with open(os.path.join(customer_dir, "customer.json"), "w") as f:
            json.dump(customer_data, f, indent=4)

        click.echo(f"Customer '{name}' updated successfully.")
        return

    click.echo(f"Customer '{name}' does not exist.")

@cx.command()
def rm():
    "Delete a customer"
    name = click.prompt("Enter customer name to delete", type=str).strip()
    for category in CATEGORY_MAP.values():
        customer_dir = get_customer_dir(category, name)
        if os.path.exists(customer_dir):
            confirm = click.confirm(f"Are you sure you want to delete '{name}'?", default=False)
            if confirm:
                for root, dirs, files in os.walk(customer_dir, topdown=False):
                    for file in files:
                        os.remove(os.path.join(root, file))
                    for dir in dirs:
                        os.rmdir(os.path.join(root, dir))
                os.rmdir(customer_dir)
                click.echo(f"Customer '{name}' deleted successfully from '{category}'.")
            else:
                click.echo("Operation canceled.")
            return

    click.echo(f"Customer '{name}' does not exist.")