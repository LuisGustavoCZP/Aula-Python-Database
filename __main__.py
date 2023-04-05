"""
Main script
"""

from postgres import Postgres

postgres = Postgres()

table1 = {
    "name": "students",
    "columns": "id SERIAL PRIMARY KEY, first_name VARCHAR(120) NOT NULL, last_name VARCHAR(120) NOT NULL",
    "foreigns": [],
}

table2 = {
    "name": "modules",
    "columns": "id uuid DEFAULT gen_random_uuid() PRIMARY KEY, name VARCHAR(60) UNIQUE",
    "foreigns": [],
}

table3 = {
    "name": "students_modules",
    "columns": "student_id INTEGER NOT NULL, module_id uuid NOT NULL, PRIMARY KEY (student_id , module_id)",
    "foreigns": [
        ", FOREIGN KEY (student_id) REFERENCES students (id) ON UPDATE CASCADE ON DELETE CASCADE"
        ", FOREIGN KEY (module_id) REFERENCES modules (id) ON UPDATE CASCADE ON DELETE CASCADE"
    ],
}


def create_table(table):
    """
    Create a table in Postgres
    """
    postgres.execute(
        f'CREATE TABLE IF NOT EXISTS {table["name"]} ({table["columns"]}{" ".join(map(str, table["foreigns"]))});'
    )


def create_module(name:str):
    """
    Create some module
    """
    postgres.execute(
        f'INSERT INTO {table2["name"]} (name) VALUES (%s) RETURNING id',
    [name])
    return postgres.fetch()[0]


def create_student(first_name:str, last_name:str):
    """
    Create some student
    """
    postgres.execute(
        f'INSERT INTO {table1["name"]} (first_name, last_name) VALUES (%s, %s) RETURNING id',[first_name, last_name])
    return postgres.fetch()[0]


def join_studant_module(student_id:int, module_id:str):
    """
    Join some student with some module
    """
    postgres.execute(
        f'INSERT INTO {table3["name"]} (student_id, module_id) VALUES (%s, %s) RETURNING *',
        [student_id, module_id],
    )
    return postgres.fetch()


create_table(table1)
create_table(table2)
create_table(table3)

postgres.commit()

try:
    module1 = create_module("Banco de Dados")
    student1 = create_student("Luis Gustavo", "Zanetti")

    student_module1 = join_studant_module(student1, module1)

    postgres.commit()
except:
    postgres.rollback()

postgres.commit()
postgres.execute(f'SELECT * from {table3["name"]}')
print(postgres.fetchall())
