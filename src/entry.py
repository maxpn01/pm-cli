import utils
import vault
import json

def add_entry(name, entry_type):
    loaded_vault = vault.load_vault()

    if name in loaded_vault:
        print(f"Entry '{name}' already exists")
        return

    entry = {
        "id": utils.generate_id(),
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
    entry["created"] = utils.get_current_date()
    entry["updated"] = utils.get_current_date()

    loaded_vault[name] = entry

    vault.save_vault(loaded_vault)

    print(f"Added entry: {name}")

def edit_entry(name, modified):
    loaded_vault = vault.load_vault()

    if name not in loaded_vault:
        print(f"Entry '{name}' not found")
        return

    entry = loaded_vault[name]
    new_name = modified.pop("name", None)

    if new_name is not None and new_name in loaded_vault and new_name != name:
        print(f"Entry '{new_name}' already exists")
        return

    for field, value in modified.items():
        entry[field] = value

    entry["updated"] = utils.get_current_date()

    if new_name is not None:
        entry["name"] = new_name
        loaded_vault[new_name] = entry
        del loaded_vault[name]

    vault.save_vault(loaded_vault)

    print(f"Edited entry: {new_name or name}")

def delete_entry(name):
    loaded_vault = vault.load_vault()

    if name not in loaded_vault:
        print(f"Entry '{name}' not found")
        return

    del loaded_vault[name]

    vault.save_vault(loaded_vault)

    print(f"Deleted entry: {name}")

def show_entry(name):
    loaded_vault = vault.load_vault()

    if name not in loaded_vault:
        print(f"Entry '{name}' not found")
        return

    entry = loaded_vault[name]

    hidden_fields = {"id", "type", "created", "updated"}
    visible_entry = {
        key: value
        for key, value in entry.items()
        if key not in hidden_fields
    }

    print(json.dumps(visible_entry, indent=2))
