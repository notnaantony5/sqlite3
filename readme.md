# Задание

Написать программу, которая по запросу создает таблицы,
генерирует данные и заполняет их.
Для генерации данных можно занести примеры в списки и выбирать их случайно
(randint, choice, shuffle из библиотеки random)
В таблицах должна хранится следующая информация
Информация о сотруднике (имя, возраст, текущую должность, начало карьеры и другое).
У каждого сотрудника есть набор навыков
(Python, SQL, HTML, JS, Django, FastAPI, Git)
Программа должна по запросу, содержащему необходимые навыки и опыт работы, выбрать из базы и показать
наиболее подходящих кандидатов, (от 50%)

Пользователь:
```shell
Навыки:
Python, sql, GIT
Опыт работы, лет:
5
```
Программа:
```shell
Вот наиболее подходящие кандидаты:

    1. Александр, 6 лет опыт работы,
    Навыки: Python, Git, Django
    Подходит на 66%.
    
    2. Антон, 3 года...
```
Навыки: Python, Git, Django -> ['python', 'sql', 'git']
person <-> job
person <- person_skill_link (person_id, skill_id) - skill
```python
persons = dict()
for skill in skills (['python', 'sql', 'git']):
    for person in persons (SELECT * from person)
        for person_skill in person_skills (
SELECT * from skill, person_skill_link
WHERE person.id = person_skill_link.person_id
AND person_skill_link.skill_id = skill.id
)
        if person_skill.name == skill:
            if dct.get(person_id):
                dct[person_id] += 1
            else:
                dct[person_id] = 1
```
        

