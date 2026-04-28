import json
import uuid
import argparse
from pathlib import Path
from datetime import datetime, timezone

VAULT_PATH = Path("vault.json")

# UTILS

def generate_id():
    return str(uuid.uuid4())

def now_date():
    return datetime.now(timezone.utc).date().isoformat()

def build_parser():
    parser = argparse.ArgumentParser(prog="pm")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("gen")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("name")
    add_type = add_parser.add_mutually_exclusive_group(required=True)
    add_type.add_argument("--login", action="store_const", const="login", dest="entry_type")
    add_type.add_argument("--secret", action="store_const", const="secret", dest="entry_type")

    edit_parser = subparsers.add_parser("edit")
    edit_parser.add_argument("entry_name")
    edit_parser.add_argument("--name")
    edit_parser.add_argument("--username")
    edit_parser.add_argument("--email")
    edit_parser.add_argument("--password")
    edit_parser.add_argument("--url")
    edit_parser.add_argument("--notes")
    edit_parser.add_argument("--secret-note", dest="secret_note")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("name")

    return parser

def get_modified_fields(args):
    fields = ("name", "username", "email", "password", "url", "notes", "secret_note")
    return {
        field: getattr(args, field)
        for field in fields
        if getattr(args, field) is not None
    }

# VAULT FUNCTIONS

def gen_vault():
    if VAULT_PATH.exists():
        print("Vault already exists")
        return

    save_vault({})
    print("Vault created")

def load_vault():
    if not VAULT_PATH.exists():
        return {}

    return json.loads(VAULT_PATH.read_text(encoding="utf-8"))

def save_vault(vault):
    VAULT_PATH.write_text(
        json.dumps(vault, indent=2),
        encoding="utf-8"
    )

# ENTRY FUNCTIONS

def add_entry(name, entry_type):
    vault = load_vault()

    if name in vault:
        print(f"Entry '{name}' already exists")
        return

    entry = {
        "id": generate_id(),
        "name": name,
        "type": entry_type,
    }

    if entry_type == "login":
        entry["username"] = input("Username: ").strip() or None
        entry["email"] = input("Email: ").strip() or None
        entry["password"] = input("Password: ").strip() or None
        entry["url"] = input("URL: ").strip() or None
    else:
        entry["secret_note"] = input("Secret: ").strip() or None

    entry["notes"] = input("Notes: ") or None
    entry["created_at"] = now_date()
    entry["updated_at"] = now_date()

    vault[name] = entry

    save_vault(vault)

    print(f"Added entry: {name}")

def edit_entry(name, modified):
    vault = load_vault()

    if name not in vault:
        print(f"Entry '{name}' not found")
        return

    entry = vault[name]
    new_name = modified.pop("name", None)

    if new_name is not None and new_name in vault and new_name != name:
        print(f"Entry '{new_name}' already exists")
        return

    for field, value in modified.items():
        entry[field] = value

    entry["updated_at"] = now_date()

    if new_name is not None:
        entry["name"] = new_name
        vault[new_name] = entry
        del vault[name]

    save_vault(vault)

    print(f"Edited entry: {new_name or name}")

def delete_entry(name):
    vault = load_vault()

    if name not in vault:
        print(f"Entry '{name}' not found")
        return

    del vault[name]

    save_vault(vault)

    print(f"Deleted entry: {name}")

# MAIN

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "gen":
        gen_vault()
    elif args.command == "add":
        add_entry(args.name, args.entry_type)
    elif args.command == "edit":
        modified_fields = get_modified_fields(args)

        if not modified_fields:
            parser.error("edit requires at least one field to update")

        edit_entry(args.entry_name, modified_fields)
    elif args.command == "delete":
        delete_entry(args.name)


if __name__ == "__main__": 
    main()
