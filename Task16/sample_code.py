import os
import sqlite3

# 🔴 Hardcoded secret
API_KEY = "sk-1234567890abcdef"

def get_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # 🔴 SQL Injection vulnerability
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)

    return cursor.fetchall()


def login(username, password):
    # 🔴 Hardcoded credentials
    if username == "admin" and password == "admin123":
        return True
    return False


def run_command():
    cmd = input("Enter command: ")

    # 🔴 Unsafe function (command injection)
    os.system(cmd)


def unsafe_eval():
    data = input("Enter something: ")

    # 🔴 Dangerous eval usage
    result = eval(data)
    print(result)


def insecure_file_read(filename):
    # 🔴 Path traversal risk
    with open("/home/user/" + filename, "r") as f:
        return f.read()