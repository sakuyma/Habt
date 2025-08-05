import winreg
import sys
import os

def add_to_context_menu(program_name, program_path, file_types="*", icon_path=None):
    """
    Добавляет программу в контекстное меню Windows
    
    :param program_name: Название пункта меню
    :param program_path: Полный путь к исполняемому файлу
    :param file_types: Типы файлов ("*" - все, ".txt" - только txt и т.д.)
    :param icon_path: Путь к иконке (None - использовать иконку программы)
    :return: True если успешно, False если ошибка
    """
    try:
        # Открываем нужный раздел реестра
        key_path = f"{file_types}\\shell\\{program_name}"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
            winreg.SetValue(key, '', winreg.REG_SZ, f"Открыть в {program_name}")
            
            # Добавляем иконку если указана
            if icon_path:
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_path)
        
        # Создаем команду для выполнения
        command_path = f"{file_types}\\shell\\{program_name}\\command"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_path) as key:
            winreg.SetValue(key, '', winreg.REG_SZ, f'"{program_path}" "%1"')
        
        return True
    except Exception as e:
        pass
        return False

def remove_from_context_menu(program_name, file_types="*"):
    """
    Удаляет программу из контекстного меню Windows
    
    :param program_name: Название пункта меню для удаления
    :param file_types: Типы файлов ("*" - все, ".txt" - только txt и т.д.)
    :return: True если успешно, False если ошибка
    """
    try:
        key_path = f"{file_types}\\shell\\{program_name}"
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
        return True
    except Exception as e:
        pass
        return False

if __name__ == "__main__":
    # Пример использования
    if not sys.platform == "win32":
        print("Этот скрипт работает только в Windows!")
        sys.exit(1)
    
    # Проверяем права администратора
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "", 0, winreg.KEY_WRITE):
            pass
    except PermissionError:
        sys.exit(1)
    
    # Настройки
    program_name = "file_copy_util.py"
    program_path = os.path.abspath("file_copy_util.exe")  # Путь к вашей программе
    file_types = "*"  # Для всех файлов
    # file_types = ".txt"  # Только для текстовых файлов
    
    # Добавляем в меню
    if add_to_context_menu(program_name, program_path, file_types):
        pass
    else:
        pass
    
    # Чтобы удалить:
    # remove_from_context_menu(program_name, file_types)