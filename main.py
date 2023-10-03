import subprocess
import time
import sys

def run_program():
    while True:
        try:
            # Здесь вызывается ваша программа
            subprocess.run([sys.executable, "main_bot.py"])
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            # Ждем некоторое время перед повторным запуском (например, 5 секунд)
            time.sleep(5)
            print("Перезапуск программы...")

if __name__ == "__main__":
    run_program()