# Файл main.py (точка входа в приложение)
from clock_app import create_app

def main():
    app, root = create_app()
    root.mainloop()

if __name__ == "__main__":
    main()