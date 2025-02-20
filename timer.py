import tkinter as tk
from threading import Timer

class MultiThreadedTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Многопоточный Таймер")
        self.root.geometry("300x200")

        self.label = tk.Label(root, text="Введите секунды:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack(pady=5)

        self.start_button = tk.Button(root, text="Старт", command=self.start_timer, font=("Arial", 12))
        self.start_button.pack(pady=10)

        self.time_label = tk.Label(root, text="", font=("Arial", 14))
        self.time_label.pack(pady=10)

        self.timer = None

    def start_timer(self):
        try:
            seconds = int(self.entry.get())
            self.time_label.config(text=f"Ожидание {seconds} секунд...")
            self.timer = Timer(seconds, self.time_up)
            self.timer.start()
        except ValueError:
            self.time_label.config(text="Введите число!")

    def time_up(self):
        self.time_label.config(text="Время вышло!")

def run_timer():
    root = tk.Tk()
    app = MultiThreadedTimer(root)
    root.mainloop()
