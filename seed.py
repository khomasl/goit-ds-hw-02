import faker
from random import randint
import sqlite3

NUMBER_USERS = 10
NUMBER_STATUS = 3
NUMBER_TASKS = 20


def prepare_data(numbers_users, number_tasks) -> tuple:
    fake_data = faker.Faker()

    for_users = []
    for _ in range(numbers_users):
        for_users.append(
            (
                fake_data.name(),
                fake_data.email(),
            )
        )

    for_status = [("new",), ("in progress",), ("completed",)]

    for_tasks = []
    for _ in range(number_tasks):
        for_tasks.append(
            (
                fake_data.text(max_nb_chars=15),
                fake_data.text(max_nb_chars=40),
                randint(1, NUMBER_STATUS),
                randint(1, NUMBER_USERS),
            )
        )

    return for_users, for_status, for_tasks


def insert_data_to_db(users, status, tasks) -> None:
    # Створимо з'єднання з нашою БД та отримаємо об'єкт курсора для маніпуляцій з даними
    with sqlite3.connect("tsm.db") as con:

        cur = con.cursor()

        """Заповнюємо таблицю користувачів. І створюємо скрипт для вставлення, де змінні, які вставлятимемо, помітимо
        знаком заповнювача (?) """

        sql_to_users = """INSERT INTO users(fullname, email)
                            VALUES (?, ?)"""

        """Для вставлення відразу всіх даних скористаємося методом executemany курсора. Першим параметром буде текст
        скрипту, а другим - дані (список кортежів)."""

        cur.executemany(sql_to_users, users)

        # Далі вставляємо дані про статуси. Напишемо для нього скрипт і вкажемо змінні
        sql_to_status = """INSERT INTO status(name)
                            VALUES (?)"""

        cur.executemany(sql_to_status, status)

        # Останньою заповнюємо таблицю із задачами
        sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id)
                            VALUES (?, ?, ?, ?)"""

        cur.executemany(sql_to_tasks, tasks)

        # Фіксуємо наші зміни в БД
        con.commit()


if __name__ == "__main__":
    users, status, tasks = prepare_data(NUMBER_USERS, NUMBER_TASKS)
    # print("users: ", users)
    # print("status: ", status)
    # print("tasks: ", tasks)
    insert_data_to_db(users, status, tasks)
