import sys
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone

VAULT_PATH = Path("vault.json")

# UTILS

def generate_id():
    return str(uuid.uuid4())

def now_date():
    return datetime.now(timezone.utc).date()

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

def parse_add_args(args):
    valid_flags = {"--login", "--secret"}
    names = [arg for arg in args if not arg.startswith("--")]
    flags = [arg for arg in args if arg.startswith("--")]

    if len(names) != 1 or any(flag not in valid_flags for flag in flags):
        return None, None

    has_login = "--login" in args
    has_secret = "--secret" in args

    if has_login == has_secret:
        return None, None

    return names[0], "login" if has_login else "secret"

def add_entry(name, entry_type):
    vault = load_vault()

    if name in vault:
        print(f"Entry '{name}' already exists")
        return

    entry = {
        "id": generate_id(),
        "name": name,
        "type": entry_type,
        "created_at": now_date(),
        "updated_at": now_date(),
    }

    if entry_type == "login":
        entry["username"] = input("Username: ").strip() or None
        entry["email"] = input("Email: ").strip() or None
        entry["password"] = input("Password: ").strip() or None
        entry["url"] = input("URL: ").strip() or None
    else:
        entry["secret"] = input("Secret: ").strip() or None

    entry["notes"] = input("Notes: ") or None

    vault[name] = entry

    save_vault(vault)

    print(f"Added entry: {name}")

# MAIN

def main():
    args = sys.argv[1:]

    if not args:
        print("usage: python main.py <command>")
        return

    command = args[0]

    if command == "gen":
        gen_vault()
    elif command == "add":
        name, entry_type = parse_add_args(args[1:])

        if name is None:
            print("Usage: python main.py add <name> (--login | --secret)")
            return
        
        add_entry(name, entry_type)
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__": 
    main()
