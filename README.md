# pm

`pm` is a small local CLI password manager. It stores entries in an encrypted
`vault.json` file in the directory where you run the command.

The project is intentionally simple: no accounts, no sync service, no browser
extension, and no cloud backend.

Built for fun and as a way to learn how password managers work internally.

## Features

- Encrypted local vault file
- Master password unlock
- Argon2id key derivation for new vaults
- Backward-compatible PBKDF2 vault reading
- Login and secret entries
- Entry add, edit, show, list, and delete commands
- Master password rotation
- Secure random password generation

## Install

Install the project from the repo:

```bash
python3 -m pip install .
```

For local development, the repo also includes a launcher:

```bash
ln -sf "$(pwd)/bin/pm" "$HOME/.local/bin/pm"
```

Make sure `~/.local/bin` is in your shell path:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then verify:

```bash
pm help
```

## Usage

Create a new encrypted vault:

```bash
pm init
```

Add a login:

```bash
pm add --login github
```

Add a secret:

```bash
pm add --secret api-key-openai
```

Show one entry:

```bash
pm show github
```

List all entries:

```bash
pm list
```

Edit an entry:

```bash
pm edit github --email alice@example.com
pm edit github --password new-password
pm edit github --url https://github.com
```

Delete an entry:

```bash
pm delete github
```

Change the master password:

```bash
pm password
```

Generate a password:

```bash
pm gen --length 16 --uppercase --lowercase --numbers --symbols
```

Delete the vault file:

```bash
pm erase
```

Show command help:

```bash
pm
pm help
pm --help
```

## Vault Format

The plaintext vault data is a Python dictionary serialized as JSON before
encryption. On disk, `vault.json` stores an encrypted envelope:

```json
{
  "version": 1,
  "kdf": "argon2id",
  "time_cost": 3,
  "memory_cost": 65536,
  "parallelism": 4,
  "salt": "...",
  "ciphertext": "..."
}
```

The actual entries are inside `ciphertext`.

## Security Model

`pm` uses:

- `getpass` for hidden master password prompts
- Argon2id to derive an encryption key from the master password
- a random salt for key derivation
- `cryptography.fernet` for authenticated encryption
- Python's `secrets` module for password generation

This protects the vault file if someone obtains `vault.json` but does not know
the master password.

This project does not currently provide:

- automatic locking for a long-running session
- clipboard clearing
- multi-device sync
- two-factor authentication
- recovery keys
- secure sharing
- protection from malware or a compromised machine
