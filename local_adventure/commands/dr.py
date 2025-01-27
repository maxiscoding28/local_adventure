import os
import click

@click.group(context_settings={"max_content_width": 220})
def dr():
    pass

@dr.command(context_settings={"max_content_width": 220})
def tree():
    import os

    base_dir = os.path.expanduser("~/.local_adventure")
    required_structure = {
        "primary": ["cx"],
        "secondary": ["cx"],
        "tertiary": ["cx"],
    }
    errors = []
    required_paths = set()

    # Build the set of required paths
    for section, subdirs in required_structure.items():
        for subdir in subdirs:
            required_paths.add(os.path.join(base_dir, section, subdir))
        # Add the section directories (e.g., primary, secondary, tertiary)
        required_paths.add(os.path.join(base_dir, section))

    # Check for missing directories
    for path in required_paths:
        if not os.path.exists(path):
            errors.append(f"🔴 Missing directory: {path}")

    # Validate unexpected directories only at the first level of `cx`
    for root, dirs, _ in os.walk(base_dir):
        # Determine the current level being checked
        rel_root = os.path.relpath(root, base_dir)
        if rel_root == ".":
            valid_dirs = required_structure.keys()
        elif rel_root in required_structure:
            valid_dirs = ["cx"]
        else:
            continue

        for dir_name in dirs:
            if dir_name not in valid_dirs:
                full_path = os.path.join(root, dir_name)
                errors.append(f"🔴 Unexpected directory: {os.path.abspath(full_path)}")

    if errors:
        for error in errors:
            print(error)
    else:
        print("🟢 All directories are valid.")

@dr.command(context_settings={"max_content_width": 220})
def cx():
    base_dir = os.path.expanduser("~/.local_adventure")
    errors = []

    for category in ["primary", "secondary", "tertiary"]:
        cx_dir = os.path.join(base_dir, category, "cx")
        if not os.path.exists(cx_dir):
            errors.append(f"🔴 Missing directory: {cx_dir}")
            continue

        customers = os.listdir(cx_dir)
        if not customers:
            print(f"🟡 No customers exist in directory: {cx_dir}")
            continue

        for customer_dir in customers:
            customer_path = os.path.join(cx_dir, customer_dir)
            if not os.path.isdir(customer_path):
                errors.append(f"🔴 Not a directory: {customer_path}")
                continue

            customer_json = os.path.join(customer_path, "customer.json")
            if not os.path.isfile(customer_json):
                errors.append(f"🔴 Missing customer.json: {customer_json}")

    if errors:
        for error in errors:
            print(error)
    else:
        print("🟢 All customer.json files are valid.")

@dr.command(context_settings={"max_content_width": 220})
def tx():
    base_dir = os.path.expanduser("~/.local_adventure")
    errors = []

    for category in ["primary", "secondary", "tertiary"]:
        for status in ["open", "closed"]:
            tx_dir = os.path.join(base_dir, category, "tx", status)
            if not os.path.exists(tx_dir):
                errors.append(f"🔴 Missing directory: {tx_dir}")
                continue

            tickets = os.listdir(tx_dir)
            if not tickets:
                print(f"🟡 No tickets exist in directory: {tx_dir}")
                continue

            for ticket_dir in tickets:
                ticket_path = os.path.join(tx_dir, ticket_dir)
                if not os.path.isdir(ticket_path):
                    errors.append(f"🔴 Not a directory: {ticket_path}")
                    continue

                ticket_json = os.path.join(ticket_path, "ticket.json")
                if not os.path.isfile(ticket_json):
                    errors.append(f"🔴 Missing ticket.json: {ticket_json}")