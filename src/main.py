import sys
from pathlib import Path

def gen_vault():
    vault_path = Path("vault.json")
    
    if vault_path.exists():
        print("Vault already exists")
        return

    vault_path.write_text("{}", encoding="utf-8")
    print("Vault created: vault.json")

def main():
    args = sys.argv[1:]

    if not args:
        print("usage: python main.py <command>")
        return

    command = args[0]

    if command == "gen":
        gen_vault()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__": 
    main()