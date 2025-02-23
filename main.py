import tkinter as tk
from tkinter import ttk, messagebox
import time

class TimerFrame(tk.Frame):
    def __init__(self, parent, timer_label="Timer"):
        super().__init__(parent, bg="black")
        self.timer_label = timer_label

        # Custom fonts
        self.custom_font = ("Helvetica", 30, "bold")
        self.name_font = ("Helvetica", 16, "bold")
        self.button_font = ("Helvetica", 12)

        # Timer name display label (initially empty)
        self.timer_name_label = tk.Label(self, text="", font=self.name_font, bg="black", fg="white")
        self.timer_name_label.pack(pady=5)

        # Countdown display label
        self.label = tk.Label(self, text="00:00", font=self.custom_font, bg="black", fg="white")
        self.label.pack(pady=10)

        # Progress bar styling (darker yellow)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("yellow.Horizontal.TProgressbar",
                             troughcolor="gray20",
                             background="#B8860B",  # Darker yellow
                             thickness=20)
        self.progress = ttk.Progressbar(self, style="yellow.Horizontal.TProgressbar",
                                        orient='horizontal', length=250, mode='determinate')
        self.progress.pack(pady=10)

        # Input frame for timer name and seconds
        input_frame = tk.Frame(self, bg="black")
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Timer Name:", font=("Helvetica", 12),
                 bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = tk.Entry(input_frame, font=("Helvetica", 12),
                                   bg="gray20", fg="white", insertbackground="white", justify="center")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(input_frame, text="Seconds:", font=("Helvetica", 12),
                 bg="black", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry = tk.Entry(input_frame, font=("Helvetica", 12),
                              bg="gray20", fg="white", insertbackground="white", justify="center")
        self.entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons for controlling the timer
        self.start_button = tk.Button(self, text="Start", font=self.button_font,
                                      command=self.start_timer, bg="gray20", fg="white",
                                      activebackground="gray30", activeforeground="white")
        self.start_button.pack(pady=5)
        self.pause_button = tk.Button(self, text="Pause", font=self.button_font,
                                      command=self.toggle_pause, state='disabled',
                                      bg="gray20", fg="white",
                                      activebackground="gray30", activeforeground="white")
        self.pause_button.pack(pady=5)
        self.reset_button = tk.Button(self, text="Reset", font=self.button_font,
                                      command=self.reset_timer, state='disabled',
                                      bg="gray20", fg="white",
                                      activebackground="gray30", activeforeground="white")
        self.reset_button.pack(pady=5)

        # Timer state variables
        self.total_seconds = 0
        self.timer_running = False
        self.paused = False
        self.end_time = None
        self.remaining = 0

    def update_timer(self):
        if not self.timer_running:
            return

        if not self.paused:
            now = time.time()
            self.remaining = self.end_time - now
            if self.remaining <= 0:
                self.label.config(text="00:00")
                self.progress['value'] = self.total_seconds
                messagebox.showinfo(self.timer_label, "Time's up!")
                self.timer_running = False
                self.pause_button.config(state='disabled')
                self.reset_button.config(state='disabled')
                return
            else:
                # Smoothly update the progress bar based on elapsed time
                progress_value = self.total_seconds - self.remaining
                self.progress['value'] = progress_value
                # Update the countdown display in whole seconds
                secs = int(self.remaining)
                mins, sec = divmod(secs, 60)
                self.label.config(text=f"{mins:02}:{sec:02}")
        self.after(50, self.update_timer)

    def start_timer(self):
        if self.timer_running:
            return
        try:
            seconds = int(self.entry.get())
            if seconds <= 0:
                messagebox.showerror(self.timer_label, "Please enter a positive number!")
                return
            # Set and display the timer name
            timer_name = self.name_entry.get().strip()
            self.timer_name_label.config(text=timer_name)
            self.total_seconds = seconds
            self.timer_running = True
            self.paused = False
            self.pause_button.config(text="Pause", state='normal')
            self.reset_button.config(state='normal')
            self.progress['maximum'] = seconds
            self.progress['value'] = 0
            self.end_time = time.time() + seconds
            self.update_timer()
        except ValueError:
            messagebox.showerror(self.timer_label, "Please enter a number!")

    def toggle_pause(self):
        if not self.timer_running:
            return
        if self.paused:
            # Resume timer by recalculating the end time
            self.paused = False
            self.pause_button.config(text="Pause")
            self.end_time = time.time() + self.remaining
        else:
            self.paused = True
            self.pause_button.config(text="Resume")

    def reset_timer(self):
        self.timer_running = False
        self.paused = False
        self.total_seconds = 0
        self.end_time = None
        self.remaining = 0
        self.label.config(text="00:00")
        self.progress['value'] = 0
        self.pause_button.config(state='disabled')
        self.reset_button.config(state='disabled')
        self.timer_name_label.config(text="")

def main():
    root = tk.Tk()
    root.title("Timer Launcher")
    root.geometry("400x500")
    root.configure(bg="black")

    # Create a Notebook (tabbed interface) to hold three different timers
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Create three TimerFrame instances (they can be customized further if needed)
    timer1 = TimerFrame(notebook, timer_label="Timer 1")
    timer2 = TimerFrame(notebook, timer_label="Timer 2")
    timer3 = TimerFrame(notebook, timer_label="Timer 3")

    notebook.add(timer1, text="Timer 1")
    notebook.add(timer2, text="Timer 2")
    notebook.add(timer3, text="Timer 3")

    root.mainloop()

if __name__ == "__main__":
    main()
