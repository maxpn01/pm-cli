import json
from pathlib import Path

VAULT_PATH = Path("vault.json")

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

