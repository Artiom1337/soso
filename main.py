import threading
import tkinter as tk
from timer_vanea import TimerApp as TimerVaneaApp
from timer_artiom import TimerApp as TimerArtiomApp
from timer_foca import TimerApp as TimerFocaApp

def start_vanea_timer():
    root_vanea = tk.Tk()
    app_vanea = TimerVaneaApp(root_vanea)
    root_vanea.mainloop()


def start_artiom_timer():
    root_artiom = tk.Tk()
    app_artiom = TimerArtiomApp(root_artiom)
    root_artiom.mainloop()


def start_foca_timer():
    root_foca = tk.Tk()
    app_foca = TimerFocaApp(root_foca)
    root_foca.mainloop()

if __name__ == "__main__":
    # Запуск таймеров в отдельных потоках
    threading.Thread(target=start_vanea_timer, daemon=True).start()
    threading.Thread(target=start_artiom_timer, daemon=True).start()
    threading.Thread(target=start_foca_timer, daemon=True).start()

    # Основной цикл для поддержания работы всех окон
    # Этот основной поток не должен завершаться, иначе окна закроются
    tk.Tk().mainloop()  # Это обеспечит работу всех окон
