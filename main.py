import sqlite3
from typing import NamedTuple

DROP = False


def main():
    with sqlite3.connect('data.db') as conn:
        if DROP:
            cur = conn.cursor()
            cur.execute("DROP TABLE IF EXISTS users")
            cur.execute("DROP TABLE IF EXISTS profiles")
            conn.commit()
        users_profiles = get_data_from_db(conn)
        for user in users_profiles:
            print_profile(user)
        # create_tables(conn)
        # user = get_user_data()
        # profile = get_profile_data()
        # insert_into_user_table(conn, user)
        # insert_into_profile_table(conn, profile)


class UserProfileData(NamedTuple):
    name: str
    age: int
    title: str
    content: str


def print_profile(profile: UserProfileData):
    print(f"Имя: {profile.name}\n"
          f"Возраст: {profile.age}\n"
          f"Название: {profile.title}\n"
          f"Содержание: {profile.content}\n")


def get_data_from_db(conn: sqlite3.Connection) -> list[UserProfileData]:
    cur = conn.cursor()
    get_data = ("SELECT users.id, users.name, users.age, "
                "profiles.title, profiles.content, profiles.user_id "
                "FROM users, profiles "
                "WHERE users.id = profiles.user_id")
    data = cur.execute(get_data).fetchall()
    return [
        UserProfileData(name, age, title, content)
        for _, name, age, title, content, _ in data
    ]


class UserData(NamedTuple):
    name: str
    age: int


class ProfileData(NamedTuple):
    title: str
    content: str
    user_id: int


def get_user_data() -> UserData:
    name = input('Введите свое имя: ')
    age = int(input('Введите свой возраст: '))
    return UserData(name=name, age=age)


def get_profile_data() -> ProfileData:
    title = input('Введите название профайла: ')
    content = input('Введите содержимое: ')
    user_id = int(input('Введите user_id: '))
    return ProfileData(title=title, content=content, user_id=user_id)


def insert_into_user_table(conn: sqlite3.Connection,
                           user: UserData):
    cursor = conn.cursor()
    insert_command = ("INSERT INTO users (name, age) "
                      "VALUES (?, ?)")
    cursor.execute(insert_command,
                   (user.name, user.age))
    conn.commit()


def insert_into_profile_table(conn: sqlite3.Connection,
                              profile: ProfileData):
    cursor = conn.cursor()
    insert_command = ("INSERT INTO profiles (title, content, user_id) "
                      "VALUES (?, ?, ?)")
    cursor.execute(insert_command,
                   profile)
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
    create_profile_table = (
        "CREATE TABLE IF NOT EXISTS profiles "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "title VARCHAR(30) NOT NULL, "
        "content TEXT NOT NULL, "
        "user_id INTEGER, "
        "FOREIGN KEY (user_id) REFERENCES users(id)) "
    )
    cursor.execute(create_profile_table)
    conn.commit()


if __name__ == "__main__":
    main()
