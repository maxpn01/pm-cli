.PHONY: install uninstall

install:
	mkdir -p "$(HOME)/.local/bin"
	ln -sf "$(CURDIR)/bin/pm" "$(HOME)/.local/bin/pm"
	chmod +x "$(CURDIR)/bin/pm"
	@echo "Installed pm to $(HOME)/.local/bin/pm"

uninstall:
	rm -f "$(HOME)/.local/bin/pm"
	@echo "Uninstalled pm"
