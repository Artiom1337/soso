import threading
import tkinter as tk
from datetime import datetime


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi Timer App")

        self.label = tk.Label(root, text="00:00:00", font=("Arial", 24))
        self.label.pack(pady=20)

        self.interval_label = tk.Label(root, text="Interval (seconds):")
        self.interval_label.pack()
        self.interval_entry = tk.Entry(root)
        self.interval_entry.pack()

        self.duration_label = tk.Label(root, text="Duration (seconds):")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(root)
        self.duration_entry.pack()

        self.remaining_label = tk.Label(root, text="Time left: ", font=("Arial", 18))
        self.remaining_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Timer", command=self.start_timer)
        self.start_button.pack()

        self.running = False
        self.time_left = 0

    def update_label(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.label.config(text=current_time)
        if self.running:
            self.root.after(1000, self.update_label)  # Обновление каждую секунду

    def update_remaining_time(self):
        if self.time_left > 0:
            self.remaining_label.config(text=f"Time left: {self.time_left} sec")
            self.time_left -= 1
            self.root.after(1000, self.update_remaining_time)
        else:
            self.remaining_label.config(text="Time left: 0 sec")
            self.stop_timer()

    def run_task(self, duration):
        print("Task executed")
        self.time_left = duration
        self.update_remaining_time()

    def start_timer(self):
        try:
            interval = int(self.interval_entry.get())
            duration = int(self.duration_entry.get())

            if interval > 0 and duration > 0:
                self.running = True
                self.update_label()
                threading.Timer(interval, self.run_task, args=(duration,)).start()
        except ValueError:
            print("Please enter valid numbers.")

    def stop_timer(self):
        self.running = False
        print("Timer stopped")


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()