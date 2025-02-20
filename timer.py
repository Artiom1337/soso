import tkinter as tk
from tkinter import messagebox

def start_timer():
    try:
        time_left = int(entry.get())
        countdown(time_left)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите число!")

def countdown(time_left):
    if time_left > 0:
        mins, secs = divmod(time_left, 60)
        label.config(text=f"{mins:02}:{secs:02}")
        root.after(1000, countdown, time_left - 1)
    else:
        label.config(text="00:00")
        messagebox.showinfo("Таймер", "Время вышло!")

root = tk.Tk()
root.title("Таймер")

label = tk.Label(root, text="00:00", font=("Arial", 30))
label.pack()

entry = tk.Entry(root)
entry.pack()

btn = tk.Button(root, text="Старт", command=start_timer)
btn.pack()

root.mainloop()
