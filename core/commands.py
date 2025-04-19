import os

def load_commands():
    """Загрузка команд"""
    commands_file = "Scripts/commands.txt"
    default_commands = {
        "help": "Show command list",
        "mods": "Show mods list",
        "get gui": "Show in GUI",
        "clear": "Clear console",
        "settings": "System settings",
        "settings text color [color]": "Change text color",
        "exit": "Exit",
        "backup": "Create backup",
        "catt": "Show mods in catalyst",
        "version": "System version"
    }

    if not os.path.exists(commands_file):
        try:
            with open(commands_file, "w", encoding="utf-8") as f:
                for cmd, desc in default_commands.items():
                    f.write(f"{cmd}\t| {desc}\n")
            return list(default_commands.items())
        except Exception as e:
            print(f"[Error] Failed to create commands.txt: {e}")
            return list(default_commands.items())

    encodings = ['utf-8', 'cp1251', 'utf-16-le']
    for encoding in encodings:
        try:
            commands = []
            with open(commands_file, "r", encoding=encoding) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split("\t| ")
                        if len(parts) >= 2:
                            commands.append((parts[0], " | ".join(parts[1:])))
            if commands:
                return commands
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"[Error] Reading commands.txt: {e}")
            continue

    print("[NOTICE] Creating new command file...")
    try:
        with open(commands_file, "w", encoding="utf-8") as f:
            for cmd, desc in default_commands.items():
                f.write(f"{cmd}\t| {desc}\n")
        return list(default_commands.items())
    except Exception as e:
        print(f"[CRITICAL] Failed to create commands.txt: {e}")
        return [("help", "Показать справку"), ("exit", "Выход")]