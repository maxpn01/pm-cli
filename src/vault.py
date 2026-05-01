import json
import base64
import getpass
import os
import sys
from pathlib import Path
from argon2.low_level import Type, hash_secret_raw
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VAULT_PATH = Path("vault.json")
VAULT_VERSION = 1
KDF = "argon2id"
ARGON2_TIME_COST = 3
ARGON2_MEMORY_COST = 64 * 1024
ARGON2_PARALLELISM = 4
PBKDF2_KDF = "pbkdf2-sha256"
PBKDF2_ITERATIONS = 600_000

_master_password = None
_envelope = None

def gen_vault():
    if VAULT_PATH.exists():
        print("Vault already exists")
        return

    password = prompt_new_master_password()
    save_encrypted_vault({}, password)
    print("Vault created")

def load_vault():
    if not VAULT_PATH.exists():
        print("Vault does not exist. Run 'pm init' first.")
        sys.exit(1)

    try:
        vault_file = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Vault file is not valid JSON")
        sys.exit(1)

    if not is_encrypted_vault(vault_file):
        return migrate_plaintext_vault(vault_file)

    password = getpass.getpass("Master password: ")
    return decrypt_vault(vault_file, password)

def save_vault(vault):
    if _master_password is None:
        print("Vault is locked")
        sys.exit(1)

    save_encrypted_vault(vault, _master_password)

def save_encrypted_vault(vault, password):
    global _envelope

    salt = get_salt()
    fernet = Fernet(derive_argon2id_key(password, salt))
    plaintext = json.dumps(vault).encode("utf-8")
    ciphertext = fernet.encrypt(plaintext).decode("utf-8")

    encrypted_vault = {
        "version": VAULT_VERSION,
        "kdf": KDF,
        "time_cost": ARGON2_TIME_COST,
        "memory_cost": ARGON2_MEMORY_COST,
        "parallelism": ARGON2_PARALLELISM,
        "salt": base64.b64encode(salt).decode("utf-8"),
        "ciphertext": ciphertext,
    }

    VAULT_PATH.write_text(
        json.dumps(encrypted_vault, indent=2),
        encoding="utf-8"
    )
    _envelope = encrypted_vault

def decrypt_vault(encrypted_vault, password):
    global _master_password, _envelope

    if encrypted_vault.get("version") != VAULT_VERSION:
        print("Unsupported vault version")
        sys.exit(1)

    if encrypted_vault.get("kdf") not in {KDF, PBKDF2_KDF}:
        print("Unsupported vault key derivation method")
        sys.exit(1)

    try:
        salt = base64.b64decode(encrypted_vault["salt"], validate=True)
        ciphertext = encrypted_vault["ciphertext"].encode("utf-8")
        fernet = Fernet(derive_key(password, salt, encrypted_vault))
        plaintext = fernet.decrypt(ciphertext)
        loaded_vault = json.loads(plaintext.decode("utf-8"))
    except (InvalidToken, KeyError, TypeError, ValueError, json.JSONDecodeError):
        print("Invalid master password or corrupted vault")
        sys.exit(1)

    _master_password = password
    _envelope = encrypted_vault
    return loaded_vault

def derive_key(password, salt, encrypted_vault):
    if encrypted_vault["kdf"] == KDF:
        return derive_argon2id_key(
            password,
            salt,
            encrypted_vault["time_cost"],
            encrypted_vault["memory_cost"],
            encrypted_vault["parallelism"],
        )

    if encrypted_vault["kdf"] == PBKDF2_KDF:
        return derive_pbkdf2_key(password, salt, encrypted_vault["iterations"])

    raise ValueError("unsupported key derivation method")

def derive_argon2id_key(
    password,
    salt,
    time_cost=ARGON2_TIME_COST,
    memory_cost=ARGON2_MEMORY_COST,
    parallelism=ARGON2_PARALLELISM,
):
    key = hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
        hash_len=32,
        type=Type.ID,
    )
    return base64.urlsafe_b64encode(key)

def derive_pbkdf2_key(password, salt, iterations):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

def get_salt():
    if _envelope is not None and _envelope.get("kdf") == KDF:
        return base64.b64decode(_envelope["salt"])

    return os.urandom(16)

def is_encrypted_vault(vault_file):
    base_fields = {"version", "kdf", "salt", "ciphertext"}
    return isinstance(vault_file, dict) and base_fields.issubset(vault_file)

def migrate_plaintext_vault(vault_file):
    global _master_password

    confirmation = input("vault.json is unencrypted. Encrypt it now? [y/n]: ").strip()

    if confirmation != "y":
        print("Migration cancelled")
        sys.exit(1)

    password = prompt_new_master_password()
    _master_password = password
    save_encrypted_vault(vault_file, password)
    print("Vault encrypted")
    return vault_file

def prompt_new_master_password():
    password = getpass.getpass("New master password: ")
    confirmation = getpass.getpass("Confirm master password: ")

    if not password:
        print("Master password cannot be empty")
        sys.exit(1)

    if password != confirmation:
        print("Master passwords do not match")
        sys.exit(1)

    return password

def erase_vault():
    if not VAULT_PATH.exists():
        print("Vault does not exist")
        return

    confirmation = input("Delete vault.json? [y/n]: ").strip()

    if confirmation != "y":
        print("Erase cancelled")
        return

    VAULT_PATH.unlink()
    print("Vault deleted")
