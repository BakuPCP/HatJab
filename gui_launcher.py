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
        """Обработка команд"""
        cmd = self.cmd_entry.get().strip()
        self.cmd_entry.delete(0, tk.END)

        if not cmd:
            return

        self.print_output(f"> {cmd}\n")

        try:
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
                    print(f"[Error] Failed to start GUI: {e}")
            elif cmd.startswith("settings text color"):
                self.change_text_color(cmd)
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
            elif cmd == "backup":
                self.create_backup()
            elif cmd == "catt":
                self.show_catalyst()
            elif cmd == "version":
                self.show_version()
            elif cmd == "exit":
                self.exit_program()
            else:
                self.print_output(f"Unknown command: {cmd}\nType 'help' for commands\n")
        except Exception as e:
            self.print_output(f"[Error] {str(e)}\n")

    def show_help(self):
        """Показать список команд"""
        self.print_output("\nAvailable commands:\n")
        max_len = max(len(c[0]) for c in self.commands)
        for c, d in self.commands:
            self.print_output(f"  {c.ljust(max_len)} - {d}\n")

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