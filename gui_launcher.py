import tkinter as tk
from tkinter import ttk, scrolledtext
import os
import shutil
from datetime import datetime
from System import catal, hjcheck, crypto
from core.commands import load_commands
from core.settings_manager import settings_manager


class HatJabGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HatJab GUI v1.0")
        self.root.geometry("1000x600")
        self.root.configure(bg='#333333')

        # Инициализация компонентов
        self.catal = catal
        self.commands = load_commands()

        # Цветовая схема
        self.bg_color = '#333333'
        self.frame_color = '#555555'
        self.text_color = '#FFFFFF'
        self.input_color = '#444444'

        self.setup_ui()
        self.print_welcome()

    def setup_ui(self):
        """Настройка интерфейса"""
        # Основной фрейм
        self.output_frame = tk.Frame(self.root, bg=self.frame_color, bd=2, relief=tk.RAISED)
        self.output_frame.pack(fill=tk.BOTH, expand=True, padx=300, pady=10)

        # Текстовое поле
        self.output_text = scrolledtext.ScrolledText(
            self.output_frame,
            bg=self.input_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            wrap=tk.WORD,
            font=('Consolas', 10)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output_text.configure(state='disabled')

        # Фрейм ввода
        self.input_frame = tk.Frame(self.root, bg=self.bg_color)
        self.input_frame.pack(fill=tk.X, padx=400, pady=(0, 10))

        # Поле ввода
        self.cmd_entry = tk.Entry(self.input_frame, font=('Consolas', 10))
        self.cmd_entry.pack(fill=tk.X, expand=True)
        self.cmd_entry.bind('<Return>', self.execute_command)
        self.cmd_entry.focus_set()

        #self.cmd_entry = ttk.Combobox(self.input_frame, font=('Consolas', 10))
        #self.cmd_entry.pack(fill=tk.X, expand=True)
        #self.cmd_entry.bind('<Return>', self.execute_command)
        #self.cmd_entry.bind('<KeyRelease>', self.update_autocomplete)
        #self.cmd_entry.focus_set()

    #def update_autocomplete(self, event):
    #    """Обновление списка автодополнения"""
    #    current_text = self.cmd_entry.get()
    #    if not current_text:
    #        return
        # Загружаем команды из commands.txt
    #    with open("Scripts/commands.txt", "r", encoding="utf-8") as f:
    #        commands = [line.split("\t| ")[0] for line in f]
        # Фильтруем команды по введенному тексту
    #    matches = [cmd for cmd in commands if cmd.startswith(current_text)]
    #    if matches:
    #        self.cmd_entry['values'] = matches

    def print_output(self, text):
        """Вывод текста в интерфейс"""
        self.output_text.configure(state='normal')
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state='disabled')
        self.output_text.see(tk.END)

    def print_welcome(self):
        """Приветственное сообщение"""
        welcome_msg = """
██╗  ██╗ █████╗ ████████╗     ██╗  █████╗ ██████╗  
██║  ██║██╔══██╗╚══██╔══╝     ██║ ██╔══██╗██╔══██╗  
███████║███████║   ██║        ██║ ███████║██████╔╝  
██╔══██║██╔══██║   ██║   ██   ██║ ██╔══██║██╔══██╗  
██║  ██║██║  ██║   ██║   ╚█████╔╝ ██║  ██║██████╔╝  
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚════╝  ╚═╝  ╚═╝╚═════╝  

Welcome to HatJab GUI v1.0!
Type 'help' for available commands
"""
        self.print_output(welcome_msg)

    def execute_command(self, event=None):
        """Обработка команд (расширенная версия)"""
        cmd = self.cmd_entry.get().strip()
        self.cmd_entry.delete(0, tk.END)

        if not cmd:
            return

        self.print_output(f"> {cmd}\n")

        # Обработка алиасов (как в main_loop.py)
        aliases = settings_manager.handle_aliases("list")
        cmd_lower = cmd.lower()
        if cmd_lower.split()[0] in aliases:
            alias_cmd = aliases[cmd_lower.split()[0]]
            cmd = alias_cmd + " " + " ".join(cmd_lower.split()[1:])

        try:
            # Переносим логику из handle_command() в main_loop.py
            if cmd == "help":
                self.show_help()
            elif cmd == "mods":
                self.show_mods()
            elif cmd == "clear":
                self.clear_console()
            elif cmd == "settings":
                try:
                    from Scripts.settings import start_editor
                    start_editor()
                except Exception as e:
                    self.print_output(f"[Error] Failed to start GUI settings editor: {e}\n")
            elif cmd.startswith("settings --first-start"):
                mode = cmd.split()[-1].lower()
                if mode in ["gui", "console"]:
                    new_settings = settings_manager.settings.copy()
                    new_settings["first_start"] = mode
                    if settings_manager.save_settings(new_settings):
                        print(f"\nStartup mode set to: {mode}")
                    else:
                        print("\nFailed to save settings")
                else:
                    print("\nInvalid mode. Use 'gui' or 'console'")
            elif cmd.startswith("settings alias"):
                args = cmd.split()[2:]
                if not args or args[0] == "help":
                    self.print_output("\nUsage:\n")
                    self.print_output("  settings alias list          - Show all aliases\n")
                    self.print_output("  settings alias [name=cmd]   - Create alias\n")
                    self.print_output("  settings alias [name]=      - Remove alias\n")
                elif args[0] == "list":
                    aliases = settings_manager.handle_aliases("list")
                    self.print_output("\nAliases:\n" if aliases else "\nNo aliases defined\n")
                    for name, cmd in aliases.items():
                        self.print_output(f"  {name.ljust(10)} = {cmd}\n")
                elif "=" in args[0]:
                    alias, _, command = args[0].partition("=")
                    if not alias:
                        self.print_output("\nError: Alias name cannot be empty\n")
                    elif command:
                        if settings_manager.handle_aliases("set", alias, command):
                            self.print_output(f"\nAlias set: {alias} = {command}\n")
                        else:
                            self.print_output("\nFailed to set alias\n")
                    else:
                        if settings_manager.handle_aliases("remove", alias):
                            self.print_output(f"\nAlias removed: {alias}\n")
                        else:
                            self.print_output("\nAlias not found\n")
                else:
                    self.print_output("\nInvalid syntax. Use 'name=command'\n")
            elif cmd.startswith("settings autosave"):
                args = cmd.split()[2:]
                if not args or args[0] == "help":
                    self.print_output("\nUsage:\n")
                    self.print_output("  settings autosave on [interval]  - Enable autosave\n")
                    self.print_output("  settings autosave off           - Disable autosave\n")
                else:
                    new_settings = settings_manager.settings.copy()
                    if args[0] == "on":
                        new_settings["autosave"] = True
                        if len(args) > 1 and args[1].isdigit():
                            new_settings["autosave_interval"] = int(args[1])
                        self.print_output("\nAutosave enabled\n")
                    elif args[0] == "off":
                        new_settings["autosave"] = False
                        self.print_output("\nAutosave disabled\n")
                    else:
                        self.print_output("\nInvalid argument. Use 'on' or 'off'\n")
                        return
                    if not settings_manager.save_settings(new_settings):
                        self.print_output("\nFailed to save settings\n")
            elif cmd.startswith("settings env"):
                args = cmd.split()[2:]
                if not args or args[0] == "help":
                    self.print_output("\nUsage:\n")
                    self.print_output("  settings env list                   - Show all variables\n")
                    self.print_output("  settings env get [VAR]              - Get value\n")
                    self.print_output("  settings env set [VAR] [VALUE]      - Set value\n")
                    self.print_output("  settings env unset [VAR]            - Remove variable\n")
                else:
                    action = args[0]
                    if action == "list":
                        env_vars = settings_manager.handle_env_vars("list")
                        self.print_output("\nEnvironment variables:\n")
                        for k, v in env_vars.items():
                            self.print_output(f"  {k}={v}\n")
                    elif action == "get" and len(args) >= 2:
                        value = settings_manager.handle_env_vars("get", args[1])
                        self.print_output(f"\n{args[1]}={value}\n")
                    elif action == "set" and len(args) >= 3:
                        if settings_manager.handle_env_vars("set", args[1], " ".join(args[2:])):
                            self.print_output(f"\nSet: {args[1]}={' '.join(args[2:])}\n")
                        else:
                            self.print_output("\nSetting error\n")
                    elif action == "unset" and len(args) >= 2:
                        if settings_manager.handle_env_vars("unset", args[1]):
                            self.print_output(f"\nRemoved: {args[1]}\n")
                        else:
                            self.print_output("\nRemoval error\n")
                    else:
                        self.print_output("\nInvalid arguments. Use 'settings env help'\n")
            elif cmd.startswith("settings text color"):
                color = cmd.split()[-1].lower()
                if settings_manager.save_color(color):
                    self.text_color = {
                        'green': '#00FF00',
                        'lightblue': '#ADD8E6',
                        'purple': '#800080',
                        'default': '#FFFFFF'
                    }[color]
                    self.output_text.configure(fg=self.text_color)
                    self.print_output(f"\nText color changed to {color}\n")
                else:
                    self.print_output("\nAvailable colors: green, lightblue, purple, default\n")
            elif cmd == "catt":
                self.show_catalyst()
            elif cmd == "version":
                self.show_version()
            elif cmd == "reboot":
                self.print_output("\n[System] Restarting GUI...\n")
                self.root.destroy()
                launch_gui()  # Перезапуск GUI
            elif cmd == "exit":
                self.exit_program()
            elif cmd == "backup":
                self.create_backup()
            else:
                self.print_output(f"\nUnknown command: {cmd}\nType 'help' for commands\n")
        except Exception as e:
            self.print_output(f"[Error] {str(e)}\n")

    def show_help(self):
        """Показать список всех команд"""
        self.print_output("\nAvailable commands:\n")
        with open("Scripts/commands.txt", "r", encoding="utf-8") as f:
            for line in f:
                cmd, desc = line.strip().split("\t| ")
                self.print_output(f"  {cmd.ljust(20)} - {desc}\n")

    def show_mods(self):
        """Показать список модов"""
        mods = hjcheck.list_mods(return_list=True)
        self.print_output("\nInstalled mods:\n" if mods else "\nNo mods installed\n")
        for mod in mods:
            self.print_output(f"- {mod}\n")

    def clear_console(self):
        """Очистить консоль"""
        self.output_text.configure(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state='disabled')

    def show_settings(self):
        """Показать настройки"""
        self.print_output("\nSettings options:\n")
        self.print_output("1. Text color (green/lightblue/purple/default)\n")
        self.print_output("2. Editor type\n")
        self.print_output("Usage: 'settings text color <color>'\n")

    def change_text_color(self, cmd):
        color = cmd.split()[-1].lower()
        if settings_manager.save_color(color):
            self.text_color = {
                'green': '#00FF00',
                'lightblue': '#ADD8E6',
                'purple': '#800080',
                'default': '#FFFFFF'
            }[color]
            self.output_text.configure(fg=self.text_color)
            self.print_output(f"Text color changed to {color}\n")
        else:
            self.print_output("Available colors: green, lightblue, purple, default\n")

    def create_backup(self):
        """Создать резервную копию"""
        try:
            backup_dir = "Backups"
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"

            important_files = [
                "Data/ps.dhj",
                "Data/rep.dhj",
                "Data/session.seshj",
                "Data/rsa_keys.keyhj",
                "Scripts/commands.txt",
                "Scripts/settings.cfg"
            ]

            temp_dir = f"temp_backup_{timestamp}"
            os.makedirs(temp_dir, exist_ok=True)

            for file in important_files:
                if os.path.exists(file):
                    shutil.copy2(file, os.path.join(temp_dir, os.path.basename(file)))

            shutil.make_archive(os.path.join(backup_dir, backup_name), "zip", temp_dir)
            shutil.rmtree(temp_dir)
            self.print_output("[Success] Backup created successfully\n")
        except Exception as e:
            self.print_output(f"[Error] Backup failed: {str(e)}\n")

    def show_catalyst(self):
        """Показать содержимое catalyst"""
        if not self.catal:
            self.print_output("[Error] Catalyst module not loaded\n")
            return

        files = self.catal.get_mod_list()
        self.print_output("\nFiles in catalyst:\n" if files else "\nCatalyst folder is empty\n")
        for f in sorted(files):
            self.print_output(f"- {f}\n")

    def show_version(self):
        """Показать версию"""
        self.print_output("\nHatJab v1.0.5\n")
        self.print_output("Mod & Encryption management System\n")

    def exit_program(self):
        """Выход из программы"""
        if self.catal and hasattr(self.catal, 'process_mods'):
            if self.catal.process_mods():
                self.print_output("\n[System] New mods installed\n")
        self.root.destroy()


def launch_gui():
    """Запуск графического интерфейса"""
    root = tk.Tk()
    app = HatJabGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()