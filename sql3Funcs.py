import sqlite3

def create_table(path, table_name, **columns):
    columns = list(columns.items())
    primary_column = ' '.join(columns[0])
    other_columns = ''

    iteration = -1

    for column in columns:
        iteration += 1

        if iteration == 0:
            continue

        other_columns += ' '.join(column) + ', '

    else:
        other_columns = other_columns[:-2]

    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()

        cursor.execute(f'''CREATE TABLE IF NOT EXISTS
                       {table_name}({primary_column} PRIMARY KEY, {other_columns})''')

def insert_into_table(path, table_name, **columns):
    def render(value):
        return f'"{value}"'

    keys = ', '.join(list(columns.keys()))
    values = ', '.join(map(render, list(columns.values())))

    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()

        cursor.execute(f'''INSERT INTO {table_name}({keys}) VALUES({values})''')

def update_table(path, table_name, *where, **updated_columns):
    updated_columns = list(updated_columns.items())

    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()

        for column in updated_columns:
            cursor.execute(f'''UPDATE {table_name} SET {column[0]}="{column[1]}" 
                           WHERE {where[0]}="{where[1]}"''')

def get_from_table(path, table_name, *where, howMany=None):
    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()

        if len(where) != 0:
            cursor.execute(f'''SELECT * FROM {table_name} WHERE {where[0]}="{where[1]}"''')

            return cursor.fetchone()

        if howMany != None:
            cursor.execute(f'''SELECT * FROM {table_name}''')

            return cursor.fetchmany(howMany)

        cursor.execute(F'''SELECT * FROM {table_name}''')

        return cursor.fetchall()

def delete_from_table(path, table_name, *where):
    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()

        if len(where) != 0:
            cursor.execute(f'''DELETE FROM {table_name} WHERE {where[0]}="{where[1]}"''')

        else:
            cursor.execute(f'''DELETE FROM {table_name}''')

# create_table('example.db', 'users',
#              id='INTEGER', fullname='TEXT', age='INT', balance='REAL')

# insert_into_table('example.db', 'users',
#                   id=1, fullname='Alex Smith', age=17, balance=100)

# insert_into_table('example.db', 'users',
#                   id=2, fullname='Pete Armstrong', age=27, balance=2452)
#
# insert_into_table('example.db', 'users',
#                   id=3, fullname='Kate Evans', age=21, balance=3241)

# update_table('example.db', 'users', 'id', 1, fullname='John Smith', balance=200)

# print(get_from_table('example.db', 'users', 'id', 2))
# print(get_from_table('example.db', 'users', howMany=2))
# print(get_from_table('example.db', 'users'))

# delete_from_table('example.db', 'users', 'id', 2)
# delete_from_table('example.db', 'users')
