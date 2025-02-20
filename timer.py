import tkinter as tk
from tkinter import messagebox
import threading
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер")
        self.root.geometry("300x200")

        self.label = tk.Label(root, text="00:00", font=("Arial", 30))
        self.label.pack(pady=20)

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.start_button = tk.Button(root, text="Старт", command=self.start_timer)
        self.start_button.pack(pady=10)

    def countdown(self, seconds):
        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            self.label.config(text=f"{mins:02}:{secs:02}")
            time.sleep(1)
            seconds -= 1
        self.label.config(text="00:00")
        messagebox.showinfo("Таймер", "Время вышло!")

    def start_timer(self):
        try:
            seconds = int(self.entry.get())
            threading.Thread(target=self.countdown, args=(seconds,), daemon=True).start()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число!")

def start_gui():
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
