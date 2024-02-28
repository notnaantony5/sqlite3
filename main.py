import sqlite3
from random import choice, randint, shuffle

SKILLS = ['python', 'sql', 'git', 'django', 'fastapi']
NAMES = ['Саша', 'Петя', 'Вова', 'Егор', 'Антон']


def get_data_from_user() -> tuple[list[str], int]:
    skills_str = input("Введите навыки через запятую:\n")
    exp = int(input("Введите стаж:\n"))
    skills = [word.strip()
              for word in
              skills_str.lower().split(',')]
    return skills, exp


def get_data_from_db(
        conn: sqlite3.Connection,
        skills: list[str],
        exp: int
):
    persons_skills = dict()
    get_persons_id = """
    SELECT id FROM person
    """
    cur = conn.cursor()
    cur.execute(get_persons_id)
    persons_ids = [person_id[0]
                   for person_id in cur.fetchall()]
    for person_id in persons_ids:
        get_person_skills = """
            SELECT * from skill, person_skill_link, person
            WHERE person_skill_link.person_id = ?
            AND person_skill_link.skill_id = skill.id
            AND person_skill_link.person_id = person.id
            AND person.exp > ?
            """  # TODO: добавить второй вопрос (значение)
        cur.execute(get_person_skills, (person_id, exp))
        db_skills = cur.fetchall()
        for skill in skills:
            for db_skill in db_skills:
                if skill == db_skill[1]:
                    if persons_skills.get(person_id):
                        persons_skills[person_id] += 1
                    else:
                        persons_skills[person_id] = 1
    persons_skills = [{"person_id": person_id, "skills_count": skills_count}
                      for person_id, skills_count
                      in persons_skills.items()]
    persons_skills.sort(key=lambda x: x["skills_count"], reverse=True)
    persons_skills = persons_skills[:3]
    for person in persons_skills:
        get_user_info = """
        SELECT name, age, exp
        FROM person
        WHERE id = ?
        """  # TODO: брать не только имя а все поля таблицы
        cur.execute(get_user_info, (person['person_id'],))
        name, age, exp = cur.fetchone()
        person['name'] = name
        person['age'] = age
        person['exp'] = exp
    return persons_skills


def print_user_info(persons_skills, skills_count):
    for person in persons_skills:
        print(f"Имя: {person['name']}\n"
              f"Возраст: {person['age']}\n"
              f"Стаж: {person['exp']}\n"
              f"Подходит на "
              f"{person['skills_count'] * 100 // skills_count}"
              f"%.\n")  # TODO: печатать все переданные поля таблицы


def create_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    create_person = """
    CREATE TABLE IF NOT EXISTS person (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30) NOT NULL,
    age INTEGER NOT NULL,
    exp INTEGER NOT NULL
    )
    """  # TODO: Добавить поле стажа (ну и возможно возраста для полноты данных)
    create_skills = """
    CREATE TABLE IF NOT EXISTS skill (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30)
    )
    """
    create_link = """
    CREATE TABLE IF NOT EXISTS person_skill_link (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    person_id INTEGER REFERENCES person(id),
    skill_id INTEGER REFERENCES skill(id)
    )
    """
    cur.execute(create_person)
    cur.execute(create_skills)
    cur.execute(create_link)
    conn.commit()


def insert_values(conn: sqlite3.Connection):
    cur = conn.cursor()
    for skill in SKILLS:
        insert_skills = """
        INSERT INTO skill (name)
        VALUES (?)
        """
        cur.execute(insert_skills, (skill,))
    skills_ids = list(range(1, len(SKILLS) + 1))
    for person_id in range(1, 5):
        name = choice(NAMES)
        age = randint(20, 40)
        exp = randint(0, 10)
        insert_person = """
        INSERT INTO person (name, age, exp)
        VALUES (?, ?, ?)
        """  # TODO: добавить поля согласно таблице
        cur.execute(insert_person, (name, age, exp))
        # TODO: добавить соответствующие значения,
        #  числа можно сгенерировать с помощью randint
        insert_link = """
        INSERT INTO person_skill_link (person_id, skill_id)
        VALUES (?, ?)
        """
        count_skills = randint(2, 5)
        shuffle(skills_ids)
        for i in range(count_skills):
            skill_id = skills_ids[i]
            cur.execute(insert_link, (person_id, skill_id))
        conn.commit()


with sqlite3.connect('db.sqlite3') as conn:
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS person")
    cur.execute("DROP TABLE IF EXISTS skill")
    cur.execute("DROP TABLE IF EXISTS person_skill_link")
    create_tables(conn)
    insert_values(conn)
    skills, exp = get_data_from_user()
    persons_skills = get_data_from_db(conn, skills, exp)
    print_user_info(persons_skills, len(skills))
