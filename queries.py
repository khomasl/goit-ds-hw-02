import sqlite3
from colorama import Fore, Style


def execute_query(sql: str) -> list:
    with sqlite3.connect("tsm.db") as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql_queries = {
    "All tasks user 2": """
        SELECT title, description
        FROM tasks
        WHERE user_id = 2 ;
    """,
    "Tasks with status 'new'": """
        SELECT title, description
        FROM tasks
        WHERE status_id IN (
            SELECT id
            FROM status
            WHERE name = "new"
        );
    """,
    "Update task status": """
        UPDATE tasks SET status_id = 2
        WHERE id = 1 ;
    """,
    "Users without tasks": """
        SELECT *
        FROM users
        WHERE id NOT IN (
            SELECT user_id
            FROM tasks
        );
    """,
    "Add new task": """
        INSERT INTO tasks(title, description, status_id, user_id)
        VALUES ("New task", "Add new task", 1, 7);
    """,
    "Tasks without status 'completed'": """
        SELECT title, description
        FROM tasks
        WHERE status_id IN (1, 2);
    """,
    "Delete task by id": """
        DELETE FROM tasks
        WHERE id = 31
    """,
    "Users emails like '@example.org'": """
        SELECT *
        FROM users
        WHERE email LIKE '%@example.org';
    """,
    "Update user fullname": """
        UPDATE users SET fullname = 'Tom Franklin'
        WHERE id = 1 ;
    """,
    "Count tasks group by status": """
        SELECT COUNT(t.status_id) AS count_tasks, st.name AS status, t.status_id
        FROM tasks as t
        JOIN status as st ON st.id = t.status_id
        GROUP BY status_id;
    """,
    "Tasks, who is emails like '@example.com'": """
        SELECT u.fullname, u.email, t.title as task
        FROM users AS u
        LEFT JOIN tasks AS t ON t.user_id = u.id
        WHERE u.email LIKE '%@example.com';
    """,
    "Tasks without description": """
        SELECT *
        FROM tasks
        WHERE description = '';
    """,
    "Users and their tasks that are in 'in progress' status": """
        SELECT u.fullname, u.email, t.title AS task, t.description, st.name AS status
        FROM users AS u
        JOIN tasks AS t ON t.user_id = u.id
        JOIN status AS st ON st.id = t.status_id
        WHERE t.status_id = 2
        ORDER BY u.fullname;
    """,
    "Users and the number of their tasks": """
        SELECT u.fullname, u.email, COUNT(t.user_id) AS number_tasks
        FROM users AS u
        LEFT JOIN tasks AS t ON t.user_id = u.id
        GROUP BY t.user_id
		ORDER BY number_tasks DESC;
    """,
}

for name, sql in sql_queries.items():
    print(Fore.GREEN + f"{name}:", Fore.YELLOW + f"{execute_query(sql)}\n")

Style.RESET_ALL
