import readline

def init_autocomplete(commands: list):
    def completer(text: str, state: int):
        options = [cmd for cmd in commands if cmd.startswith(text)]
        return options[state] if state < len(options) else None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

def disable_autocomplete():
    readline.set_completer(None)