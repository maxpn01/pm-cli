import utils
import vault
import entry

def main():
    parser = utils.build_parser()
    args = parser.parse_args()

    if args.command == "gen":
        vault.gen_vault()
    elif args.command == "add":
        entry.add_entry(args.name, args.entry_type)
    elif args.command == "edit":
        entry.edit_entry(args.entry_name, utils.get_modified_fields(args, parser))
    elif args.command == "delete":
        entry.delete_entry(args.name)

if __name__ == "__main__": 
    main()
