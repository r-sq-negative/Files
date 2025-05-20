import os
import shutil
import configparser
from pathlib import Path
import platform

class FileManager:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.load_config(config_file)
        self.root_dir = Path(self.config['DEFAULT']['working_directory']).resolve()
        self.current_dir = self.root_dir
        self.setup_working_directory()

    def load_config(self, config_file):
        default_config = {'DEFAULT': {'working_directory': './file_manager_workspace'}}
        if not os.path.exists(config_file):
            self.config['DEFAULT'] = default_config['DEFAULT']
            with open(config_file, 'w') as configfile:
                self.config.write(configfile)
        else:
            self.config.read(config_file)

    def setup_working_directory(self):
        os.makedirs(self.root_dir, exist_ok=True)
        os.chdir(self.root_dir)

    def is_within_root(self, path):
        return self.root_dir in Path(path).resolve().parents or Path(path).resolve() == self.root_dir

    def create_directory(self, dir_name):
        target_path = self.current_dir / dir_name
        if not self.is_within_root(target_path):
            return "Ошибка: Нельзя выйти за пределы рабочей директории"
        try:
            os.makedirs(target_path, exist_ok=True)
            return f"Директория {dir_name} создана"
        except Exception as e:
            return f"Ошибка при создании директории: {e}"

    def delete_directory(self, dir_name):
        target_path = self.current_dir / dir_name
        if not self.is_within_root(target_path):
            return "Ошибка: Нельзя выйти за пределы рабочей директории"
        try:
            shutil.rmtree(target_path)
            return f"Директория {dir_name} удалена"
        except Exception as e:
            return f"Ошибка при удалении директории: {e}"

    def change_directory(self, path):
        target_path = self.current_dir / path if path != '..' else self.current_dir.parent
        target_path = target_path.resolve()
        if not self.is_within_root(target_path):
            return "Ошибка: Нельзя выйти за пределы рабочей директории"
        if not target_path.exists():
            return f"Ошибка: Директория {path} не существует"
        self.current_dir = target_path
        return f"Текущая директория: {self.current_dir}"

    def list_directory(self):
        result = []
        for item in self.current_dir.iterdir():
            item_type = 'DIR' if item.is_dir() else 'FILE'
            result.append(f"{item_type}\t{item.name}")
        return "\n".join(result) if result else "Директория пуста"

    def create_file(self, file_name):
        target_path = self.current_dir / file_name
        if not self.is_within_root(target_path):
            return "Ошибка: Нельзя выйти за пределы рабочей директории"
        try:
            target_path.touch()
            return f"Файл {file_name} создан"
        except Exception as e:
            return f"Ошибка при создании файла: {e}"

    def read_file(self, file_name):
        target_path = self.current_dir / file_name
        if not target_path.exists():
            return f"Ошибка: Файл {file_name} не существует"
        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Ошибка при чтении файла: {e}"

    def write_file(self, file_name, content):
        target_path = self.current_dir / file_name
        if not self.is_within_root(target_path):
            return "Ошибка: Нельзя выйти за пределы рабочей директории"
        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Файл {file_name} записан"
        except Exception as e:
            return f"Ошибка при записи файла: {e}"

    def delete_file(self, file_name):
        target_path = self.current_dir / file_name
        if not target_path.exists():
            return f"Ошибка: Файл {file_name} не существует"
        try:
            target_path.unlink()
            return f"Файл {file_name} удален"
        except Exception as e:
            return f"Ошибка при удалении файла: {e}"

    def copy_file(self, source, destination):
        src_path = self.current_dir / source
        dst_path = self.current_dir / destination
        if not src_path.exists():
            return f"Ошибка: Исходный файл {source} не существует"
        if not self.is_within_root(dst_path):
            return "Ошибка: Нельзя выйти за пределы рабочей директории"
        try:
            shutil.copy2(src_path, dst_path)
            return f"Файл {source} скопирован в {destination}"
        except Exception as e:
            return f"Ошибка при копировании файла: {e}"

    def move_file(self, source, destination):
        src_path = self.current_dir / source
        dst_path = self.current_dir / destination
        if not src_path.exists():
            return f"Ошибка: Исходный файл {source} не существует"
        if not self.is_within_root(dst_path):
            return "Ошибка: Нельзя выйти за пределы рабочей директории"
        try:
            shutil.move(src_path, dst_path)
            return f"Файл {source} перемещен в {destination}"
        except Exception as e:
            return f"Ошибка при перемещении файла: {e}"

    def rename_file(self, old_name, new_name):
        src_path = self.current_dir / old_name
        dst_path = self.current_dir / new_name
        if not src_path.exists():
            return f"Ошибка: Файл {old_name} не существует"
        if not self.is_within_root(dst_path):
            return "Ошибка: Нельзя выйти за пределы рабочей директории"
        try:
            src_path.rename(dst_path)
            return f"Файл {old_name} переименован в {new_name}"
        except Exception as e:
            return f"Ошибка при переименовании файла: {e}"

    def test_create_file():
        fm = FileManager()
        if (fm.current_dir / "test.txt").exists():
            (fm.current_dir / "test.txt").unlink()

        result = fm.create_file("test.txt")
        assert "создан" in result, f"Ожидалось сообщение о создании файла, но получено: {result}"
        assert (fm.current_dir / "test.txt").exists(), "Файл не был создан"

        # Очистка после теста
        (fm.current_dir / "test.txt").unlink()
        print("Тест успешно пройден!")

def main():
    fm = FileManager()
    # result = fm.create_file("test.txt")
    commands = {
        'mkdir': lambda args: fm.create_directory(args[0]) if args else "Укажите имя директории",
        'rmdir': lambda args: fm.delete_directory(args[0]) if args else "Укажите имя директории",
        'cd': lambda args: fm.change_directory(args[0]) if args else fm.change_directory('.'),
        'dir': lambda args: fm.list_directory(),
        'touch': lambda args: fm.create_file(args[0]) if args else "Укажите имя файла",
        'cat': lambda args: fm.read_file(args[0]) if args else "Укажите имя файла",
        'write': lambda args: fm.write_file(args[0], ' '.join(args[1:])) if len(args) > 1 else "Укажите имя файла и содержимое",
        'rm': lambda args: fm.delete_file(args[0]) if args else "Укажите имя файла",
        'cp': lambda args: fm.copy_file(args[0], args[1]) if len(args) == 2 else "Укажите исходный и целевой файлы",
        'mv': lambda args: fm.move_file(args[0], args[1]) if len(args) == 2 else "Укажите исходный и целевой файлы",
        'rename': lambda args: fm.rename_file(args[0], args[1]) if len(args) == 2 else "Укажите старое и новое имя файла",
        'help': lambda args: "\n".join([
            "Доступные команды:",
            "mkdir <name> - создать директорию",
            "rmdir <name> - удалить директорию",
            "cd <path> - сменить директорию",
            "dir - показать содержимое директории",
            "touch <name> - создать файл",
            "cat <name> - прочитать файл",
            "write <name> <content> - записать в файл",
            "rm <name> - удалить файл",
            "cp <source> <dest> - копировать файл",
            "mv <source> <dest> - переместить файл",
            "rename <old> <new> - переименовать файл",
            "help - показать справку",
            "exit - выйти"
        ]),
        'exit': lambda args: exit()
    }

    print("Файловый менеджер. Введите 'help' для списка команд.")
    while True:
        try:
            cmd_input = input(f"{fm.current_dir}> ").strip().split()
            if not cmd_input:
                continue
            cmd, *args = cmd_input
            if cmd in commands:
                print(commands[cmd](args))
            else:
                print(f"Неизвестная команда: {cmd}. Введите 'help' для списка команд.")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()