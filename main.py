import sqlite3
from typing import NamedTuple

DROP = False


def main():
    with sqlite3.connect('data.db') as conn:
        if DROP:
            return
        create_tables(conn)
        user_data = get_user_data()
        insert_into_user_table(conn, user_data)


class UserData(NamedTuple):
    name: str
    age: int


def get_user_data() -> UserData:
    name = input('Введите свое имя: ')
    age = int(input('Введите свой возраст: '))
    return UserData(name=name, age=age)


def insert_into_user_table(conn: sqlite3.Connection,
                           user: UserData):
    cursor = conn.cursor()
    insert_command = ("INSERT INTO users (name, age) "
                      "VALUES (?, ?)")
    cursor.execute(insert_command,
                   (user.name, user.age))
    conn.commit()


def create_tables(conn: sqlite3.Connection):
    cursor = conn.cursor()
    create_user_table = (
        "CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name VARCHAR(30) NOT NULL, "
        "age INTEGER NOT NULL)"
    )
    cursor.execute(create_user_table)
    conn.commit()


if __name__ == "__main__":
    main()
