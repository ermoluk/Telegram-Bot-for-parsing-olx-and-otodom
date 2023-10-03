import subprocess
import time
import sys

def run_program():
    while True:
        try:
            # Here, your program is called
            subprocess.run([sys.executable, "bot.py"])
        except Exception as e:
            print(f"An error occurred: {e}")
            # Wait for some time before attempting to restart (e.g., 5 seconds)
            time.sleep(5)
            print("Restarting the program...")

if __name__ == "__main__":
    run_program()
