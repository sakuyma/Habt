import keyboard
import pyperclip
import time
import configparser
import os
from datetime import datetime

# Глобальные переменные
saved_text = ""
CONFIG_FILE = "config.ini"
DEFAULT_HOTKEY = "ctrl+m"
DEFAULT_MARKDOWN_FOLDER = r"C:\Obsidian\Daily"  # Абсолютный путь


def load_config():
    """Загружает конфиг или создает новый с настройками по умолчанию"""
    config = configparser.ConfigParser()

    if not os.path.exists(CONFIG_FILE):
        config["SETTINGS"] = {
            "hotkey": DEFAULT_HOTKEY,
            "markdown_folder": DEFAULT_MARKDOWN_FOLDER
        }
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
    else:
        config.read(CONFIG_FILE)

    return {
        "hotkey": config["SETTINGS"].get("hotkey", DEFAULT_HOTKEY),
        "markdown_folder": config["SETTINGS"].get("markdown_folder", DEFAULT_MARKDOWN_FOLDER)
    }


def save_selected_text():
    """Копирует выделенный текст и сохраняет его"""
    global saved_text
    old_clipboard = pyperclip.paste()

    try:
        keyboard.send("ctrl+c")
        time.sleep(0.1)
        new_text = pyperclip.paste()

        if new_text.strip():
            saved_text = new_text
            save_to_markdown(saved_text)

    finally:
        pyperclip.copy(old_clipboard)


def save_to_markdown(text, config=None):
    """Сохраняет текст в markdown файл"""
    if config is None:
        config = load_config()

    # Создаем папку если нужно
    os.makedirs(config["markdown_folder"], exist_ok=True)

    # Генерируем имя файла на основе текущей даты
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{current_date}.md"
    filepath = os.path.join(config["markdown_folder"], filename)

    # Записываем в файл
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(text + "\n\n")
    except Exception:
        pass


def main():
    config = load_config()
    keyboard.add_hotkey(config["hotkey"], save_selected_text)
    keyboard.wait()


if __name__ == "__main__":
    main()