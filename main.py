import sqlite3
from random import choice, randint, shuffle

SKILLS = ['python', 'sql', 'git', 'django']
NAMES = ['Саша', 'Петя', 'Вова', 'Егор']


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
            SELECT * from skill, person_skill_link
            WHERE person_skill_link.person_id = ?
            AND person_skill_link.skill_id = skill.id
            """
            cur.execute(get_person_skills, (person_id,))
            db_skills = cur.fetchall()
            for skill in skills:
                for db_skill in db_skills:
                    print(skill, db_skill[1])
                    if skill == db_skill[1]:
                        if persons_skills.get(person_id):
                            persons_skills[person_id] += 1
                        else:
                            persons_skills[person_id] = 1
    print(persons_skills)


def create_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    create_person = """
    CREATE TABLE IF NOT EXISTS person (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30) NOT NULL
    )
    """
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
    for person_id in range(1, 3):
        name = choice(NAMES)
        insert_person = """
        INSERT INTO person (name)
        VALUES (?)
        """
        cur.execute(insert_person, (name,))
        insert_link = """
        INSERT INTO person_skill_link (person_id, skill_id)
        VALUES (?, ?)
        """
        count_skills = randint(2, 4)
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
    get_data_from_db(conn, skills, exp)
