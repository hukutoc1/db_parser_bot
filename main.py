from database_funcs import database_create, db_colomn_add


'''
EXAMPLE of using imported functions
columns = [{'NAME': 'id',
            'TYPE': 'INTEGER',
            'NOT NULL': True,
            'UNIQUE': True,
            'AUTOINCREMENT': True}]

database_create('2.db', 'Main',columns)

new_column = {'NAME': 'number',
              'TYPE': 'INTEGER',
              'NOT NULL': True,}

db_colomn_add('2.db', 'Main', new_column)'''
