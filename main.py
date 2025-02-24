import threading
import tkinter as tk
from timer_vanea import TimerApp as TimerVaneaApp
from timer_artiom import TimerApp as TimerArtiomApp
from timer_foca import TimerApp as TimerFocaApp

def start_vanea_timer():
    # Создаем отдельное окно для таймера Vanea
    root_vanea = tk.Toplevel()
    app_vanea = TimerVaneaApp(root_vanea)
    root_vanea.mainloop()

def start_artiom_timer():
    # Создаем отдельное окно для таймера Artiom
    root_artiom = tk.Toplevel()
    app_artiom = TimerArtiomApp(root_artiom)
    root_artiom.mainloop()

def start_foca_timer():
    # Создаем отдельное окно для таймера Foca
    root_foca = tk.Toplevel()
    app_foca = TimerFocaApp(root_foca)
    root_foca.mainloop()

if __name__ == "__main__":
    # Создаем основное окно, оно будет держать все другие окна в себе
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно, оно нам не нужно

    # Запуск таймеров в отдельных потоках
    threading.Thread(target=start_vanea_timer, daemon=True).start()
    threading.Thread(target=start_artiom_timer, daemon=True).start()
    threading.Thread(target=start_foca_timer, daemon=True).start()

    # Основной цикл
    root.mainloop()
