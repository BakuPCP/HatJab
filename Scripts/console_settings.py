import json
import os
from pathlib import Path


class ConsoleSettingsEditor:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.settings_file = self.script_dir / "settings.cfg"
        self.commands_file = self.script_dir / "commands.txt"

        self.settings = self._load_settings()
        self.commands = self._load_commands()

    def run(self):
        while True:
            print("\n=== Settings Editor ===")
            print("1. View current settings")
            print("2. Edit settings")
            print("3. View commands")
            print("4. Edit commands")
            print("5. Save and exit")
            print("6. Exit without saving")

            choice = input("Select an option: ")

            if choice == "1":
                self._show_settings()
            elif choice == "2":
                self._edit_settings()
            elif choice == "3":
                self._show_commands()
            elif choice == "4":
                self._edit_commands()
            elif choice == "5":
                self._save_all()
                break
            elif choice == "6":
                break
            else:
                print("Invalid choice, try again.")

    def _show_settings(self):
        print("\nCurrent Settings:")
        for key, value in self.settings.items():
            print(f"{key}: {value}")

    def _edit_settings(self):
        print("\nEdit Settings:")
        print(f"Current theme: {self.settings.get('theme', 'dark')}")
        theme = input("Enter new theme (light/dark): ").strip().lower()
        if theme in ["light", "dark"]:
            self.settings["theme"] = theme

        print(f"Current font size: {self.settings.get('font_size', 12)}")
        try:
            font_size = int(input("Enter new font size (8-24): "))
            if 8 <= font_size <= 24:
                self.settings["font_size"] = font_size
        except ValueError:
            print("Invalid font size, keeping current value.")

    def _show_commands(self):
        print("\nCurrent Commands:")
        for cmd in self.commands:
            print(cmd)

    def _edit_commands(self):
        print("\nEdit Commands (enter 'done' to finish):")
        new_commands = []
        while True:
            cmd = input("Enter command (form: command|description): ").strip()
            if cmd.lower() == "done":
                break
            if cmd:
                new_commands.append(cmd)
        self.commands = new_commands

    def _load_settings(self):
        if self.settings_file.exists():
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load settings: {str(e)}")
                return {"theme": "dark", "font_size": 12}
        return {"theme": "dark", "font_size": 12}

    def _load_commands(self):
        if self.commands_file.exists():
            try:
                with open(self.commands_file, "r", encoding="utf-8") as f:
                    return [line.strip() for line in f.readlines() if line.strip()]
            except Exception as e:
                print(f"Failed to load commands: {str(e)}")
                return []
        return []

    def _save_all(self):
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)

            with open(self.commands_file, "w", encoding="utf-8") as f:
                f.write("\n".join([cmd.strip() for cmd in self.commands if cmd.strip()]))

            print("Settings saved successfully!")
        except Exception as e:
            print(f"Failed to save settings: {str(e)}")

if __name__ == "__main__":
    editor = ConsoleSettingsEditor()
    editor.run()