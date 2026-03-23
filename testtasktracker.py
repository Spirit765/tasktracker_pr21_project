import pytest
import json
import os
import tkinter as tk
from unittest.mock import patch, MagicMock

# Импортировать модуль с вашим кодом
import tasktracker

@pytest.fixture(autouse=True)
def setup_and_teardown(tmp_path):
    # Создаем временные файлы для данных
    USERS_FILE = tmp_path / "users.json"
    TASKS_FILE = tmp_path / "tasks.json"
    # Записываем пустые данные
    USERS_FILE.write_text(json.dumps({}), encoding='utf-8')
    TASKS_FILE.write_text(json.dumps([]), encoding='utf-8')
    # Переназначаем пути в модуле
    tasktracker.USERS_FILE = str(USERS_FILE)
    tasktracker.TASKS_FILE = str(TASKS_FILE)
    # Загружаем данные
    tasktracker.load_data()
    # Обнуляем текущего пользователя
    tasktracker.current_user = None
    # Очищаем список задач
    tasktracker.tasks.clear()
    yield

def test_registration_success(monkeypatch):
    # Мокаем messagebox
    with patch('tasktracker.messagebox.showwarning') as mock_warn, \
         patch('tasktracker.messagebox.showinfo') as mock_info:
        # Мокаем поля ввода
        tasktracker.entry_login = MagicMock()
        tasktracker.entry_password = MagicMock()
        tasktracker.entry_login.get.return_value = 'testuser'
        tasktracker.entry_password.get.return_value = '1234'
        # Вызываем функцию регистрации
        tasktracker.register()
        # Проверяем, что пользователь добавлен
        assert 'testuser' in tasktracker.users
        assert tasktracker.users['testuser'] == '1234'
        # Проверяем, что вызвана функция info
        mock_info.assert_called_with("Успех", "Пользователь зарегистрирован")

def test_registration_short_password():
    with patch('tasktracker.messagebox.showwarning') as mock_warn:
        tasktracker.entry_login = MagicMock()
        tasktracker.entry_password = MagicMock()
        tasktracker.entry_login.get.return_value = 'user'
        tasktracker.entry_password.get.return_value = '123'
        tasktracker.register()
        mock_warn.assert_called_once_with("Ошибка", "Слишком короткий пароль")

def test_login_success(monkeypatch):
    # Добавляем пользователя
    tasktracker.users['user1'] = 'pass1'
    tasktracker.save_users()
    with patch('tasktracker.messagebox.showinfo') as mock_info, \
         patch('tasktracker.messagebox.showerror'):
        tasktracker.entry_login = MagicMock()
        tasktracker.entry_password = MagicMock()
        tasktracker.entry_login.get.return_value = 'user1'
        tasktracker.entry_password.get.return_value = 'pass1'
        tasktracker.current_user = None
        tasktracker.login()
        assert tasktracker.current_user == 'user1'
        mock_info.assert_called_with("Успех", "Вход выполнен")

def test_login_failure():
    with patch('tasktracker.messagebox.showerror') as mock_error:
        tasktracker.entry_login = MagicMock()
        tasktracker.entry_password = MagicMock()
        tasktracker.entry_login.get.return_value = 'wrong'
        tasktracker.entry_password.get.return_value = 'bad'
        tasktracker.current_user = None
        # Пользователь не существует
        tasktracker.login()
        assert tasktracker.current_user is None
        mock_error.assert_called()

def test_add_task():
    tasktracker.current_user = 'user2'
    # Мокаем поле ввода задачи
    tasktracker.entry_task = MagicMock()
    tasktracker.entry_task.get.return_value = 'Test Task'
    tasktracker.entry_task.delete = MagicMock()
    initial_len = len(tasktracker.tasks)
    tasktracker.add_task()
    assert len(tasktracker.tasks) == initial_len + 1
    last_task = tasktracker.tasks[-1]
    assert last_task['user'] == 'user2'
    assert last_task['title'] == 'Test Task'
    tasktracker.entry_task.delete.assert_called_with(0, tk.END)

def test_mark_done():
    # Добавляем задачу
    tasktracker.tasks.append({'user': 'u', 'title': 't', 'done': False})
    # Мокаем listbox.curselection
    class DummyListbox:
        def curselection(self):
            return (0,)
    tasktracker.listbox = DummyListbox()
    tasktracker.refresh_tasks = lambda: None
    tasktracker.mark_done()
    assert tasktracker.tasks[0]['done'] is True

def test_delete_task():
    # Добавляем задачу
    tasktracker.tasks.append({'user': 'u', 'title': 't', 'done': False})
    class DummyListbox:
        def curselection(self):
            return (0,)
    tasktracker.listbox = DummyListbox()
    tasktracker.refresh_tasks = lambda: None
    initial_len = len(tasktracker.tasks)
    tasktracker.delete_task()
    assert len(tasktracker.tasks) == initial_len - 1

