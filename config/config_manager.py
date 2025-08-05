# config/config_manager.py
import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path="settings.json"):
        self.config_path = Path(__file__).parent / config_path
        self.config = self._load_config()

    def _load_config(self):
        """Загружает конфиг из файла или создает новый"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            pass
        
        # Конфиг по умолчанию
        default_config = {
            "theme": {
                "accent_color": "#7f6df2",
                "bg_color": "#1a1a1a",
                "text_color": "#d9d9d9"
            },
            "settings": {
                "notifications": True,
                "auto_save": True,
                "save_to_daily_note": True,
                "font_size": 16
            }
        }
        self._save_config(default_config)
        return default_config

    def _save_config(self, config):
        """Сохраняет конфиг в файл"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_config(self):
        """Возвращает текущий конфиг"""
        return self.config

    def update_config(self, new_values):
        """Обновляет конфиг"""
        self.config = {**self.config, **new_values}
        self._save_config(self.config)
        return self.config

if __name__ == "__main__":
    # Тестирование
    manager = ConfigManager()
