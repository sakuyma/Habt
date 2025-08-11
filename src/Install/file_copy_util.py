import os
import shutil
import win32clipboard
from typing import Optional
import configparser

# Пути к конфигу (корень проекта -> папка config)
CONFIG_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  # Выходим из src в корень
    "config"                                    # Папка с конфигом
))
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")
SECTION = "context_menu"
KEY_TARGET_FOLDER = "file_folder"

def get_selected_file_in_explorer() -> Optional[str]:
    """Возвращает путь к файлу, выделенному в Проводнике Windows."""
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
            files = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
            if files and isinstance(files, tuple) and len(files) > 0:
                return files[0]
    finally:
        win32clipboard.CloseClipboard()
    return None

def load_config() -> configparser.ConfigParser:
    """Загружает конфиг из файла (или создаёт новый)."""
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE, encoding="utf-8")
    else:
        config[SECTION] = {KEY_TARGET_FOLDER: ""}
    return config

def get_target_folder() -> str:
    """Возвращает сохранённую целевую папку из конфига."""
    config = load_config()
    return config.get(SECTION, KEY_TARGET_FOLDER, fallback="")

def save_target_folder(folder_path: str) -> None:
    """Сохраняет целевую папку в конфиг."""
    config = load_config()
    if not config.has_section(SECTION):
        config.add_section(SECTION)
    config[SECTION][KEY_TARGET_FOLDER] = folder_path
    os.makedirs(CONFIG_DIR, exist_ok=True)  # Создаём папку config, если её нет
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        config.write(f)

def copy_file_to_folder(
    source_file: str,
    target_folder: Optional[str] = None,
    overwrite: bool = False
) -> str:
    """
    Копирует файл в указанную папку. Если папка не задана, берёт её из конфига.
    """
    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"Файл не найден: {source_file}")

    if target_folder is None:
        target_folder = get_target_folder()
        if not target_folder:
            raise ValueError("Целевая папка не задана в конфиге.")

    if not os.path.isdir(target_folder):
        raise NotADirectoryError(f"Папка не существует: {target_folder}")

    filename = os.path.basename(source_file)
    target_path = os.path.join(target_folder, filename)

    if not overwrite and os.path.exists(target_path):
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(target_path):
            target_path = os.path.join(target_folder, f"{base}_{counter}{ext}")
            counter += 1

    shutil.copy2(source_file, target_path)
    return target_path