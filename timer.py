import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import datetime

class MultiThreadedClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Многофункциональные часы")
        self.root.geometry("600x500")
        
        # Устанавливаем тёмно-синюю тему
        self.dark_blue = "#1a2a57"
        self.light_blue = "#3a4a77"
        self.text_color = "#ffffff"
        self.accent_color = "#4d94ff"
        
        self.root.configure(bg=self.dark_blue)
        
        # Создаем стили для виджетов
        self.style = ttk.Style()
        self.style.configure('TFrame', background=self.dark_blue)
        self.style.configure('TLabel', background=self.dark_blue, foreground=self.text_color, font=('Arial', 12))
        self.style.configure('TButton', background=self.light_blue, foreground=self.text_color, font=('Arial', 12))
        self.style.configure('Header.TLabel', background=self.dark_blue, foreground=self.accent_color, font=('Arial', 18, 'bold'))
        
        # Создаем вкладки
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Создаем фреймы для каждой вкладки
        self.clock_frame = ttk.Frame(self.notebook)
        self.alarm_frame = ttk.Frame(self.notebook)
        self.stopwatch_frame = ttk.Frame(self.notebook)
        self.timer_frame = ttk.Frame(self.notebook)
        
        # Добавляем фреймы в записную книжку
        self.notebook.add(self.clock_frame, text='Часы')
        self.notebook.add(self.alarm_frame, text='Будильник')
        self.notebook.add(self.stopwatch_frame, text='Секундомер')
        self.notebook.add(self.timer_frame, text='Таймер')
        
        # Инициализируем компоненты для каждой вкладки
        self.init_clock()
        self.init_alarm()
        self.init_stopwatch()
        self.init_timer()
        
        # Флаги и переменные для потоков
        self.clock_running = True
        self.alarm_active = False
        self.stopwatch_running = False
        self.timer_running = False
        
        # Запускаем поток часов
        self.clock_thread = threading.Thread(target=self.update_clock, daemon=True)
        self.clock_thread.start()
        
        # Обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def init_clock(self):
        # Заголовок
        self.clock_header = ttk.Label(self.clock_frame, text="Текущее время", style='Header.TLabel')
        self.clock_header.pack(pady=20)
        
        # Отображение времени
        self.time_label = ttk.Label(self.clock_frame, text="", font=('Arial', 48))
        self.time_label.pack(pady=30)
        
        # Отображение даты
        self.date_label = ttk.Label(self.clock_frame, text="", font=('Arial', 14))
        self.date_label.pack(pady=10)
    
    def init_alarm(self):
        # Заголовок
        self.alarm_header = ttk.Label(self.alarm_frame, text="Установка будильника", style='Header.TLabel')
        self.alarm_header.pack(pady=20)
        
        # Фрейм для ввода времени
        time_frame = ttk.Frame(self.alarm_frame)
        time_frame.pack(pady=20)
        
        # Часы
        ttk.Label(time_frame, text="Часы:").grid(row=0, column=0, padx=5)
        self.hour_var = tk.StringVar(value="0")
        self.hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, textvariable=self.hour_var, width=5, font=('Arial', 12))
        self.hour_spinbox.grid(row=0, column=1, padx=5)
        
        # Минуты
        ttk.Label(time_frame, text="Минуты:").grid(row=0, column=2, padx=5)
        self.minute_var = tk.StringVar(value="0")
        self.minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, textvariable=self.minute_var, width=5, font=('Arial', 12))
        self.minute_spinbox.grid(row=0, column=3, padx=5)
        
        # Кнопки управления будильником
        btn_frame = ttk.Frame(self.alarm_frame)
        btn_frame.pack(pady=20)
        
        self.set_alarm_btn = ttk.Button(btn_frame, text="Установить будильник", command=self.set_alarm)
        self.set_alarm_btn.grid(row=0, column=0, padx=10)
        
        self.cancel_alarm_btn = ttk.Button(btn_frame, text="Отменить будильник", command=self.cancel_alarm)
        self.cancel_alarm_btn.grid(row=0, column=1, padx=10)
        
        # Статус будильника
        self.alarm_status = ttk.Label(self.alarm_frame, text="Будильник не установлен", font=('Arial', 14))
        self.alarm_status.pack(pady=20)
    
    def init_stopwatch(self):
        # Заголовок
        self.stopwatch_header = ttk.Label(self.stopwatch_frame, text="Секундомер", style='Header.TLabel')
        self.stopwatch_header.pack(pady=20)
        
        # Отображение времени секундомера
        self.stopwatch_label = ttk.Label(self.stopwatch_frame, text="00:00:00.000", font=('Arial', 36))
        self.stopwatch_label.pack(pady=30)
        
        # Кнопки управления секундомером
        btn_frame = ttk.Frame(self.stopwatch_frame)
        btn_frame.pack(pady=20)
        
        self.start_stopwatch_btn = ttk.Button(btn_frame, text="Старт", command=self.start_stopwatch)
        self.start_stopwatch_btn.grid(row=0, column=0, padx=10)
        
        self.pause_stopwatch_btn = ttk.Button(btn_frame, text="Пауза", command=self.pause_stopwatch)
        self.pause_stopwatch_btn.grid(row=0, column=1, padx=10)
        
        self.reset_stopwatch_btn = ttk.Button(btn_frame, text="Сброс", command=self.reset_stopwatch)
        self.reset_stopwatch_btn.grid(row=0, column=2, padx=10)
        
        # Переменные для секундомера
        self.stopwatch_start_time = 0
        self.stopwatch_elapsed = 0
        self.stopwatch_paused_time = 0
    
    def init_timer(self):
        # Заголовок
        self.timer_header = ttk.Label(self.timer_frame, text="Таймер обратного отсчёта", style='Header.TLabel')
        self.timer_header.pack(pady=20)
        
        # Фрейм для ввода времени
        time_frame = ttk.Frame(self.timer_frame)
        time_frame.pack(pady=20)
        
        # Часы
        ttk.Label(time_frame, text="Часы:").grid(row=0, column=0, padx=5)
        self.timer_hour_var = tk.StringVar(value="0")
        self.timer_hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, textvariable=self.timer_hour_var, width=5, font=('Arial', 12))
        self.timer_hour_spinbox.grid(row=0, column=1, padx=5)
        
        # Минуты
        ttk.Label(time_frame, text="Минуты:").grid(row=0, column=2, padx=5)
        self.timer_minute_var = tk.StringVar(value="0")
        self.timer_minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, textvariable=self.timer_minute_var, width=5, font=('Arial', 12))
        self.timer_minute_spinbox.grid(row=0, column=3, padx=5)
        
        # Секунды
        ttk.Label(time_frame, text="Секунды:").grid(row=0, column=4, padx=5)
        self.timer_second_var = tk.StringVar(value="0")
        self.timer_second_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, textvariable=self.timer_second_var, width=5, font=('Arial', 12))
        self.timer_second_spinbox.grid(row=0, column=5, padx=5)
        
        # Отображение оставшегося времени
        self.timer_label = ttk.Label(self.timer_frame, text="00:00:00", font=('Arial', 36))
        self.timer_label.pack(pady=20)
        
        # Кнопки управления таймером
        btn_frame = ttk.Frame(self.timer_frame)
        btn_frame.pack(pady=20)
        
        self.start_timer_btn = ttk.Button(btn_frame, text="Старт", command=self.start_timer)
        self.start_timer_btn.grid(row=0, column=0, padx=10)
        
        self.pause_timer_btn = ttk.Button(btn_frame, text="Пауза", command=self.pause_timer)
        self.pause_timer_btn.grid(row=0, column=1, padx=10)
        
        self.reset_timer_btn = ttk.Button(btn_frame, text="Сброс", command=self.reset_timer)
        self.reset_timer_btn.grid(row=0, column=2, padx=10)
        
        # Прогресс-бар таймера
        self.timer_progress = ttk.Progressbar(self.timer_frame, orient="horizontal", length=400, mode="determinate")
        self.timer_progress.pack(pady=20)
        
        # Переменные для таймера
        self.timer_total_seconds = 0
        self.timer_remaining = 0
        self.timer_paused = False

    # Обновление часов
    def update_clock(self):
        while self.clock_running:
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M:%S")
            date_str = now.strftime("%A, %d %B %Y")
            
            # Обновляем метки времени и даты
            self.time_label.config(text=time_str)
            self.date_label.config(text=date_str)
            
            # Проверяем будильник
            if self.alarm_active:
                alarm_hour = int(self.hour_var.get())
                alarm_minute = int(self.minute_var.get())
                if now.hour == alarm_hour and now.minute == alarm_minute and now.second == 0:
                    self.trigger_alarm()
            
            time.sleep(0.5)  # Обновляем каждые 0.5 секунд
    
    # Функции для будильника
    def set_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                self.alarm_active = True
                alarm_time = f"{hour:02d}:{minute:02d}"
                self.alarm_status.config(text=f"Будильник установлен на {alarm_time}")
                
                # Запускаем отдельный поток для будильника
                alarm_thread = threading.Thread(target=self.check_alarm, args=(hour, minute), daemon=True)
                alarm_thread.start()
            else:
                messagebox.showerror("Ошибка", "Введите корректное время")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовые значения")
    
    def check_alarm(self, hour, minute):
        while self.alarm_active:
            now = datetime.datetime.now()
            if now.hour == hour and now.minute == minute and now.second == 0:
                self.trigger_alarm()
                break
            time.sleep(0.5)
    
    def trigger_alarm(self):
        # Запускаем сигнал будильника в отдельном потоке
        threading.Thread(target=self.alarm_sound, daemon=True).start()
    
    def alarm_sound(self):
        # Имитация звука будильника через всплывающее окно
        for i in range(5):  # Повторяем 5 раз
            if not self.alarm_active:
                break
            self.root.bell()  # Встроенный звук tkinter
            messagebox.showinfo("Будильник", "Время будильника!")
            time.sleep(1)
        self.alarm_active = False
        self.alarm_status.config(text="Будильник сработал")
    
    def cancel_alarm(self):
        self.alarm_active = False
        self.alarm_status.config(text="Будильник отменен")
    
    # Функции для секундомера
    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.stopwatch_start_time = time.time() - self.stopwatch_elapsed
            
            # Запускаем секундомер в отдельном потоке
            stopwatch_thread = threading.Thread(target=self.update_stopwatch, daemon=True)
            stopwatch_thread.start()
    
    def update_stopwatch(self):
        while self.stopwatch_running:
            elapsed = time.time() - self.stopwatch_start_time
            self.update_stopwatch_display(elapsed)
            time.sleep(0.01)  # Обновляем каждые 10 мс для большей точности
    
    def update_stopwatch_display(self, elapsed):
        milliseconds = int((elapsed % 1) * 1000)
        seconds = int(elapsed % 60)
        minutes = int((elapsed // 60) % 60)
        hours = int(elapsed // 3600)
        
        display = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        self.stopwatch_label.config(text=display)
    
    def pause_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_running = False
            self.stopwatch_elapsed = time.time() - self.stopwatch_start_time
    
    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0
        self.update_stopwatch_display(0)
    
    # Функции для таймера
    def start_timer(self):
        try:
            hours = int(self.timer_hour_var.get())
            minutes = int(self.timer_minute_var.get())
            seconds = int(self.timer_second_var.get())
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if total_seconds <= 0:
                messagebox.showerror("Ошибка", "Введите положительное значение времени")
                return
            
            if not self.timer_running:
                self.timer_running = True
                self.timer_paused = False
                
                if self.timer_remaining <= 0:
                    # Новый таймер
                    self.timer_total_seconds = total_seconds
                    self.timer_remaining = total_seconds
                    self.timer_progress["maximum"] = total_seconds
                
                # Запускаем таймер в отдельном потоке
                timer_thread = threading.Thread(target=self.run_timer, daemon=True)
                timer_thread.start()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовые значения")
    
    def run_timer(self):
        start_time = time.time()
        end_time = start_time + self.timer_remaining
        
        while self.timer_running and time.time() < end_time:
            if self.timer_paused:
                # Если на паузе, обновляем end_time
                remaining = end_time - time.time()
                while self.timer_paused and self.timer_running:
                    time.sleep(0.1)
                # После паузы пересчитываем end_time
                if self.timer_running:
                    end_time = time.time() + remaining
            
            # Обновляем оставшееся время
            self.timer_remaining = max(0, int(end_time - time.time()))
            self.update_timer_display()
            self.timer_progress["value"] = self.timer_total_seconds - self.timer_remaining
            
            time.sleep(0.1)
        
        # Если таймер завершился естественным образом
        if self.timer_running and self.timer_remaining <= 0:
            self.timer_complete()
    
    def update_timer_display(self):
        hours = self.timer_remaining // 3600
        minutes = (self.timer_remaining % 3600) // 60
        seconds = self.timer_remaining % 60
        
        display = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=display)
    
    def pause_timer(self):
        if self.timer_running:
            self.timer_paused = not self.timer_paused
            button_text = "Продолжить" if self.timer_paused else "Пауза"
            self.pause_timer_btn.config(text=button_text)
    
    def reset_timer(self):
        self.timer_running = False
        self.timer_paused = False
        self.timer_remaining = 0
        self.timer_label.config(text="00:00:00")
        self.timer_progress["value"] = 0
        self.pause_timer_btn.config(text="Пауза")
    
    def timer_complete(self):
        self.timer_running = False
        self.timer_label.config(text="Время вышло!")
        self.root.bell()
        threading.Thread(target=self.timer_notification, daemon=True).start()
    
    def timer_notification(self):
        messagebox.showinfo("Таймер", "Время вышло!")
    
    def on_closing(self):
        # Останавливаем все потоки при закрытии
        self.clock_running = False
        self.alarm_active = False
        self.stopwatch_running = False
        self.timer_running = False
        self.root.destroy()

def run_app():
    root = tk.Tk()
    app = MultiThreadedClockApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()