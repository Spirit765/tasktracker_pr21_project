import pytest

# Глобальные переменные, имитирующие ваши переменные из основного кода
users = {}
tasks = []
current_user = None

# Простые версии функций для тестирования
def register_user(login, password):
    global users
    if len(password) < 4:
        return False
    users[login] = password
    return True

def login_user(login, password):
    global users, current_user
    if login in users and users[login] == password:
        current_user = login
        return True
    return False

def add_task(title):
    global tasks, current_user
    if current_user is None:
        return False
    task = {"user": current_user, "title": title, "done": False}
    tasks.append(task)
    return True

@pytest.fixture(autouse=True)
def reset_globals():
    global users, tasks, current_user
    users.clear()
    tasks.clear()
    current_user = None

def test_register():
    assert register_user("alex", "1234")
    assert "alex" in users

def test_register_short_password():
    assert not register_user("alex", "123")

def test_login_success():
    register_user("alex", "1234")
    assert login_user("alex", "1234")
    assert current_user == "alex"

def test_login_failure():
    register_user("alex", "12345")
    assert not login_user("alex", "wrongpass")
    # current_user не меняется при ошибке входа
    assert current_user is None

def test_add_task():
    register_user("alex", "1234")
    login_user("alex", "1234")
    assert add_task("Test task")
    assert len(tasks) == 1
    task = tasks[0]
    assert task["title"] == "Test task"
    assert task["user"] == "alex"
    assert not task["done"]