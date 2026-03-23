import pytest
def test_tasks():
    global current_user
    global users
    global tasks
    tasks = tasks[:]
    current_user = users[current_user]
    tasks = tasks[:]
    tasks.append(current_user)
def test_users():
    global current_user
    global users
    global tasks
    tasks = tasks[:]
    current_user = users[current_user]
    users = users[:]
    tasks = tasks[:]

