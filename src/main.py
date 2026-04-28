import utils
import vault
import entry

def main():
    parser = utils.build_parser()
    args = parser.parse_args()

    if args.command == "init":
        vault.gen_vault()
    elif args.command == "add":
        entry.add_entry(args.name, args.entry_type)
    elif args.command == "edit":
        entry.edit_entry(args.entry_name, utils.get_modified_fields(args, parser))
    elif args.command == "delete":
        entry.delete_entry(args.name)
    elif args.command == "show":
        entry.show_entry(args.name)
    elif args.command == "list":
        entry.list_entries()
    elif args.command == "erase":
        vault.erase_vault()

if __name__ == "__main__": 
    main()
