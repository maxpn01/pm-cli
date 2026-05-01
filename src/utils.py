import uuid
import argparse
import secrets
import string
from datetime import datetime, timezone

def generate_id():
    return str(uuid.uuid4())

def get_current_date():
    return datetime.now(timezone.utc).date().isoformat()

def build_parser():
    parser = argparse.ArgumentParser(prog="pm")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("name")
    add_parser.set_defaults(entry_type="login")
    add_type = add_parser.add_mutually_exclusive_group()
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

    show_parser = subparsers.add_parser("show")
    show_parser.add_argument("name")

    subparsers.add_parser("list")

    subparsers.add_parser("password")

    gen_parser = subparsers.add_parser("gen")
    gen_parser.add_argument("--length", type=int, default=16)
    gen_parser.add_argument("--uppercase", action="store_true")
    gen_parser.add_argument("--lowercase", action="store_true")
    gen_parser.add_argument("--numbers", action="store_true")
    gen_parser.add_argument("--symbols", action="store_true")

    subparsers.add_parser("erase")

    return parser

def get_modified_fields(args, parser):
    fields = ("name", "username", "email", "password", "url", "notes", "secret_note")

    modified_fields = {
        field: getattr(args, field)
        for field in fields
        if getattr(args, field) is not None
    }

    if not modified_fields:
            parser.error("edit requires at least one field to update")

    return modified_fields

def generate_password(length, uppercase, lowercase, numbers, symbols):
    charsets = []

    if uppercase:
        charsets.append(string.ascii_uppercase)
    if lowercase:
        charsets.append(string.ascii_lowercase)
    if numbers:
        charsets.append(string.digits)
    if symbols:
        charsets.append(string.punctuation)

    if not charsets:
        raise ValueError("select at least one character type")

    if length < len(charsets):
        raise ValueError("length is too short for the selected character types")

    password = [secrets.choice(charset) for charset in charsets]
    all_chars = "".join(charsets)
    password.extend(secrets.choice(all_chars) for _ in range(length - len(password)))

    secrets.SystemRandom().shuffle(password)
    return "".join(password)
