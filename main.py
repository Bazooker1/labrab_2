import sqlite3
import pandas as pd

con = sqlite3.connect("studentsactivities.sqlite")
cursor = con.cursor()

def req1():  # Запрос 1.  Вывести список студентов и их групп.
    # Сортировать по возрастанию id.
    df = pd.read_sql('''
    SELECT fio, group_name FROM students
    JOIN students_group USING (id_group)
    ORDER BY id_group
    ''', con)
    print(df)
    print()


def req2():  # Запрос 2. Вывести список мероприятий, на которых были студенты,
    # занимавшие должность руководителя.
    # Сортировать по убыванию id.
    df = pd.read_sql('''
    SELECT activity_name, id_students FROM students_has_activities
    JOIN activities USING (id_activities)
    WHERE id_role = :r_id_role ORDER BY id_students DESC
    ''', con, params={"r_id_role": "0"})
    print(df)
    print()

def req3():  # Запрос 3. Вывести количество мероприятий в которых участвует каждый студент
    # Сортировать по убыванию количества.
    df = pd.read_sql('''
    SELECT fio, count(*) AS Kоличество_мероприятий  FROM students
    JOIN students_has_activities USING (id_students)
    GROUP BY id_students
    ORDER BY count(*) DESC
    ''', con)
    print(df)
    print()

def req4():  # Запрос 4. Вывести количество мероприятий каждого типа мероприятий
    # Сортировать по убыванию количества.
    df = pd.read_sql('''
    SELECT activity_name, count(*) AS Kоличество_мероприятий  FROM activities
    JOIN students_has_activities USING (id_activities)
    GROUP BY id_activities
    ORDER BY count(*) DESC
    ''', con)
    print(df)
    print()

def req5():  # Запрос 5. Удалить записи об мероприятиях, которые начались в сентябре
    cursor.execute('''
    DELETE FROM students_has_activities
    WHERE start_date LIKE '%.09.%';
    ''')
    print()

def get_students_has_activities():
    df = pd.read_sql('''
    SELECT id_activities, start_date FROM students_has_activities
    ''', con)
    print(df)
    print()

def req6():  # Запрос 6. Увеличить коэффициент организаторам и руководителям мероприятий
    cursor.execute('''
    UPDATE role
    SET role_multiplier = role_multiplier + 1
    WHERE id_role = 1 
    OR id_role = 0;
    ''')
    print()

def get_role():
    df = pd.read_sql('''
    SELECT id_role, role_name, role_multiplier FROM role
    ''', con)
    print(df)
    print()

def req7():  # Запрос 7. Вывести список ролей, у которых коэффициент выше среднего
    df = pd.read_sql('''
    SELECT  role_name, role_multiplier FROM role
    WHERE role_multiplier > (SELECT AVG(role_multiplier) FROM role)
    ''', con)
    print(df)
    print()

def req8():  # Запрос 8. Вывести список групп(ы), в которой(ых) больше всего студентов
    df = pd.read_sql('''
    SELECT  group_name, count(id_students) FROM students_group
    JOIN students USING (id_group)
    GROUP BY id_group
    HAVING count(id_students) = (
    SELECT count(id_students) 
    FROM students_group
    JOIN students USING (id_group)
    GROUP BY id_group
    ORDER BY count(id_students) desc limit 1
    )
    ''', con)
    print(df)
    print()

#req1()
req2()
#req3()
#req4()

#get_students_has_activities()
#req5()
#get_students_has_activities()

#get_role()
#req6()
#get_role()

#req7()
#req8()

