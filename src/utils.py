import uuid
import argparse
from datetime import datetime, timezone

def generate_id():
    return str(uuid.uuid4())

def get_current_date():
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