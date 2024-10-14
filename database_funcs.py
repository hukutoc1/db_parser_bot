from sqlite3 import connect


def database_create(db_name, table_name, column):
    """CREATE A NEW DATABASE 'db_name' WITH 'table_name'.
    COLUMN DEFIND LIST OF DICTIONARYS
    #[{'NAME': _NAME_, 'TYPE': _TYPE_, 'NOT NULL': True/False,
    'UNIQUE': True/False, 'AUTOINCREMENT': True/False}, ...]"""
    con = connect(f'./data/{db_name}')
    cur = con.cursor()
    autoincrement = ''
    for elem in column:
        elem['NOT NULL'] = 'NOT NULL' if elem['NOT NULL'] else ''
        elem['UNIQUE'] = 'UNIQUE' if elem['UNIQUE'] else ''
        if elem['AUTOINCREMENT'] is True:
            autoincrement = elem['NAME']
    column_request = (
        list(map(lambda x:
                 f'"{x['NAME']}" {x['TYPE']} {x['NOT NULL']} {x['UNIQUE']}',
                              column)))
    column_request = ',\n'.join(map(lambda x: x.strip(), column_request))
    database_request = (f"CREATE TABLE {table_name}"
                        f"({column_request}")
    if autoincrement:
        database_request += f',\n PRIMARY KEY ({autoincrement} AUTOINCREMENT))'
    else:
        database_request += ')'
    cur.execute(database_request)
    con.close()
    print(f'-----Database {db_name} was created') # log about database created


def db_colomn_add(db_name, table_name, new_column):
    """ADD IN DATABASE 'db_name', TABLE 'table_name' A NEW COLUMN
    'new_column'. COLUMN DEFIND DICTIONARY {'NAME': _NAME_, 'TYPE': _TYPE_,
    'NOT NULL': True/False}"""
    con = connect(f'./data/{db_name}')
    cur = con.cursor()
    new_column['NOT NULL'] = 'NOT NULL' if new_column['NOT NULL'] else ''
    column_request = (f'{new_column['NAME']} {new_column['TYPE']} '
                      f'{new_column['NOT NULL']}')
    database_req = f"ALTER TABLE {table_name} ADD COLUMN {column_request}"
    print(database_req)
    cur.execute(database_req)
    con.close()
    print(f'-----Database {db_name} was updated: add {new_column['NAME']} '
          f'column') # log about database update (add new column)
