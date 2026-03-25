import unittest

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

class TestLogic(unittest.TestCase):
    def setUp(self):
        # Обнуляем переменные перед каждым тестом
        global users, tasks, current_user
        users = {}
        tasks = []
        current_user = None

    def test_register(self):
        self.assertTrue(register_user("alex", "1234"))
        self.assertIn("alex", users)

    def test_register_short_password(self):
        self.assertFalse(register_user("alex", "123"))

    def test_login_success(self):
        register_user("alex", "1234")
        self.assertTrue(login_user("alex", "1234"))
        self.assertEqual(current_user, "alex")

    def test_login_failure(self):
        register_user("alex", "1234")
        self.assertFalse(login_user("alex", "wrongpass"))

    def test_add_task(self):
        register_user("alex", "1234")
        login_user("alex", "1234")
        self.assertTrue(add_task("Test task"))
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Test task")
        self.assertEqual(tasks[0]["user"], "alex")
        self.assertFalse(tasks[0]["done"])

if __name__ == "__main__":
    unittest.main()