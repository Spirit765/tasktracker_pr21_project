import tkinter as tk
from tkinter import messagebox
import json
import os
import logging  # ← Подключаем модуль логирования

# 🔧 Настройка логирования (минимальная конфигурация)
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"  # Для корректной записи кириллицы в лог (Python 3.9+)
)

USERS_FILE = "data/users.json"
TASKS_FILE = "data/tasks.json"

current_user = None
users = {}
tasks = []


def load_data():
    global users, tasks
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
            logging.info("Данные пользователей загружены")
        else:
            users = {}
            logging.warning("Файл пользователей не найден, создан новый")

        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                tasks = json.load(f)
            logging.info("Данные задач загружены")
        else:
            tasks = []
            logging.warning("Файл задач не найден, создан новый")
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных: {e}")
        messagebox.showerror("Ошибка", "Не удалось загрузить данные")


def save_users():
    try:
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        logging.info("Данные пользователей сохранены")
    except Exception as e:
        logging.error(f"Сбой сохранения пользователей: {e}")
        messagebox.showerror("Ошибка", "Не удалось сохранить данные пользователя")


def save_tasks():
    try:
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        logging.info("Данные задач сохранены")
    except Exception as e:
        logging.error(f"Сбой сохранения задач: {e}")
        messagebox.showerror("Ошибка", "Не удалось сохранить задачи")


def register():
    login = entry_login.get().strip()
    password = entry_password.get()

    # ⚠️ WARNING: валидация полей
    if not login:
        logging.warning("Пустое поле логина при регистрации")
        messagebox.showwarning("Ошибка", "Введите логин")
        return

    if len(password) < 4:
        logging.warning(f"Попытка регистрации с коротким паролем для пользователя: {login}")
        messagebox.showwarning("Ошибка", "Слишком короткий пароль (мин. 4 символа)")
        return

    if login in users:
        logging.warning(f"Попытка регистрации существующего пользователя: {login}")
        messagebox.showwarning("Ошибка", "Пользователь уже существует")
        return

    users[login] = password
    save_users()
    logging.info(f"Успешная регистрация пользователя: {login}")  # ✅ INFO: регистрация
    messagebox.showinfo("Успех", "Пользователь зарегистрирован")


def login():
    global current_user
    login = entry_login.get().strip()
    password = entry_password.get()

    logging.info(f"Попытка входа пользователя: {login}")  # ✅ INFO: попытка входа

    if login in users and users[login] == password:
        current_user = login
        logging.info(f"Успешный вход пользователя: {login}")  # ✅ INFO: успешный вход
        messagebox.showinfo("Успех", "Вход выполнен")
        refresh_tasks()
    else:
        logging.warning(f"Неверный логин или пароль для: {login}")  # ⚠️ WARNING: неверный ввод
        messagebox.showerror("Ошибка", "Неверный логин или пароль")


def add_task():
    if not current_user:
        logging.warning("Попытка добавить задачу без авторизации")  # ⚠️ WARNING: запрещённое действие
        messagebox.showerror("Ошибка", "Сначала войдите")
        return

    title = entry_task.get().strip()

    if not title:
        logging.warning("Пустое название задачи")  # ⚠️ WARNING: пустое поле
        messagebox.showwarning("Ошибка", "Введите название задачи")
        return

    try:
        task = {"user": current_user, "title": title, "done": False}
        tasks.append(task)
        save_tasks()  # ✅ INFO: сохранение данных внутри save_tasks()
        logging.info(f"Создана задача пользователем {current_user}: {title}")  # ✅ INFO: создание задачи
        refresh_tasks()
        entry_task.delete(0, tk.END)
    except Exception as e:
        logging.error(f"Ошибка при добавлении задачи: {e}")  # ❌ ERROR: исключение
        messagebox.showerror("Ошибка", "Не удалось добавить задачу")


def delete_task():
    if not current_user:
        logging.warning("Попытка удалить задачу без авторизации")
        messagebox.showerror("Ошибка", "Сначала войдите")
        return

    try:
        index = listbox.curselection()[0]
        deleted_task = tasks[index]["title"]
        del tasks[index]
        save_tasks()
        logging.info(f"Задача удалена пользователем {current_user}: {deleted_task}")
        refresh_tasks()
    except IndexError:
        logging.warning("Попытка удалить задачу без выделения")
        messagebox.showwarning("Ошибка", "Выберите задачу для удаления")
    except Exception as e:
        logging.error(f"Ошибка при удалении задачи: {e}")
        messagebox.showerror("Ошибка", "Не удалось удалить задачу")


def mark_done():
    if not current_user:
        logging.warning("Попытка отметить задачу без авторизации")
        messagebox.showerror("Ошибка", "Сначала войдите")
        return

    try:
        index = listbox.curselection()[0]
        task_title = tasks[index]["title"]
        tasks[index]["done"] = True
        save_tasks()
        logging.info(f"Задача отмечена выполненной пользователем {current_user}: {task_title}")
        refresh_tasks()
    except IndexError:
        logging.warning("Попытка отметить задачу без выделения")
        messagebox.showwarning("Ошибка", "Выберите задачу")
    except Exception as e:
        logging.error(f"Ошибка при изменении статуса задачи: {e}")
        messagebox.showerror("Ошибка", "Не удалось обновить задачу")


def refresh_tasks():
    listbox.delete(0, tk.END)
    for task in tasks:
        status = "[x]" if task["done"] else "[ ]"
        # Показываем только задачи текущего пользователя или все (по желанию)
        listbox.insert(tk.END, f"{status} {task['user']}: {task['title']}")


# 🚀 Запуск программы
if __name__ == "__main__":
    logging.info("=== Запуск приложения TaskTracker ===")  # ✅ INFO: запуск программы

    root = tk.Tk()
    root.title("TaskTracker")
    root.geometry("500x400")

    try:
        load_data()
    except Exception as e:
        logging.error(f"Критическая ошибка при инициализации: {e}")

    # 🔐 Интерфейс авторизации
    tk.Label(root, text="Логин").pack()
    entry_login = tk.Entry(root)
    entry_login.pack()

    tk.Label(root, text="Пароль").pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    tk.Button(root, text="Регистрация", command=register).pack(pady=5)
    tk.Button(root, text="Вход", command=login).pack(pady=5)

    # 📋 Интерфейс задач
    tk.Label(root, text="Новая задача").pack()
    entry_task = tk.Entry(root, width=40)
    entry_task.pack()

    tk.Button(root, text="Добавить задачу", command=add_task).pack(pady=5)
    tk.Button(root, text="Отметить выполненной", command=mark_done).pack(pady=5)
    tk.Button(root, text="Удалить задачу", command=delete_task).pack(pady=5)

    listbox = tk.Listbox(root, width=60, height=10)
    listbox.pack(pady=10)

    refresh_tasks()


    # Обработка закрытия окна
    def on_close():
        logging.info("Завершение работы приложения")
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()