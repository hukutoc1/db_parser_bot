import csv
import os
import json


# all imports


# ---------------------------------------------------------------------------
def configs_create(db_name, columns):
    """CREATE A JSON FILE WITH BOT CONFIGS"""
    with open('./data/configs.json', 'w') as json_f:
        configs_dict = {'DB_NAME': db_name,
                        'COLUMNS': columns}
        json.dump(configs_dict, json_f)


# ---------------------------------------------------------------------------
def get_configs_dict():
    """GET CONFIG DATA FROM JSON TO dict()"""
    if 'configs.json' in os.listdir('./data'):
        with open('./data/configs.json', 'r') as json_f:
            configs_dict = json.load(fp=json_f)
    else:
        print('DATABASE IS ABSENT')
    return configs_dict


# ---------------------------------------------------------------------------
def database_create(db_name, columns):
    """CREATE A NEW DATABASE 'db_name'. 'column' IS COLUMN NAMES FOR
    DATABASE"""
    configs_create(db_name, columns)
    with open(f'./data/{db_name}', 'w', encoding='utf-8', newline='') as db:
        dict_writer = csv.DictWriter(db, delimiter=';', quotechar='"',
                                     fieldnames=columns)
        dict_writer.writeheader()
    print(f'-----Database {db_name} was created')  # log about database created


# ---------------------------------------------------------------------------
def db_column_add(new_column):
    """ADD NEW COLUMN new_column"""
    configs_dict = get_configs_dict()
    db_name = configs_dict['DB_NAME']
    columns = configs_dict['COLUMNS'] + [new_column]
    os.remove('./data/configs.json')  # removing for creating new config file
    with open('./data/configs.json', 'w') as json_f:
        configs_dict = {'DB_NAME': db_name,
                        'COLUMNS': columns}
        json.dump(configs_dict, json_f)
    with open(f'./data/{db_name}', 'r', encoding='utf-8') as old_db:
        # taking data from database for rewriting file
        rows = list(csv.reader(old_db, delimiter=';', quotechar='"'))
    os.remove(f'./data/{db_name}')
    with open(f'./data/{db_name}', 'w', encoding='utf-8',
              newline='') as new_db:
        dict_writer = csv.DictWriter(new_db, fieldnames=columns,
                                     delimiter=';', quotechar='"')
        dict_writer.writeheader()
        for elem_dict in rows:
            elem_dict[new_column] = ''
            dict_writer.writerow(elem_dict)
    print(f'-----Database {db_name} was updated: added new'
          f'column - {new_column}')  # log about database update
    # (add new column)


# ---------------------------------------------------------------------------
def addition_rows_db(new_db_name, column_mapping, column_order):
    """ADDITION NEW ROWS FROM OTHER DATABASE WITHOUT REPETITION"""
    main_db_name = get_configs_dict()['DB_NAME']
    configs_dict = get_configs_dict()
    column = configs_dict['COLUMNS']
    with open('./data/' + main_db_name, 'r+', encoding='utf-8',
              newline='') as main_db:
        reader = list(csv.DictReader(main_db))
        dict_writer = csv.DictWriter(main_db, fieldnames=column)
        if '.db' in new_db_name:
            con_new = connect(f'./data/{new_db_name}')
            cur_new = con_new.cursor()
            new_column = ', '.join(map(lambda x: x[0], column_mapping[1:]))
            new_db_request = ('SELECT ' + new_column + ' FROM ' +
                              column_mapping[0][1])
            new_data = cur_new.execute(new_db_request).fetchall()
            for elem in new_data:
                elem_dict = {}
                for i in range(len(column)):
                    elem_dict[column[i]] = elem[column_order[i]]
                if elem_dict not in reader:
                    dict_writer.writerow(elem_dict)
        elif '.csv' in new_db_name:
            with open('./data/' + new_db_name, 'r',
                      encoding='utf-8') as new_db:
                new_data = csv.reader(new_db)
            for elem in new_data:
                elem_dict = {}
                for i in range(len(column)):
                    elem_dict[column[i]] = elem[column_order[i]]
                if elem_dict not in reader:
                    dict_writer.writerow(elem_dict)
    print(f'-----Database {main_db_name} was updated: addition '
          f'column from {new_db_name}')  # log about addition of database


# ----------------------------------------------------------------------------
def find_request(request):
    """FIND INFO IN DATABASE WITH USER REQUEST"""
    configs = get_configs_dict()
    db_name = configs['DB_NAME']
    with (open('./data/' + db_name, 'r+', encoding='utf-8',
               newline='') as main_db):
        data = list(filter(lambda x: request in x, main_db.readlines()))
        if not bool(data):
            return False
        else:
            data = list(filter(lambda x: (f';{request};' in x or
                                          x.startswith(request) or
                                          x.endswith(request)),
                               map(lambda x: x[:-2], data)))
            print(data)
            return '\n'.join(data)


if __name__ == '__main__':
    # database_create('new.csv', ['1', '12'])
    db_column_add('skrngs')
    with open('./data/new.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=get_configs_dict()['COLUMNS'],
                                delimiter=';')
        writer.writerow({'1': 12, '12': 123, 'skrngs': 3865})
        writer.writerow({'1': 11, '12': 123, 'skrngs': 3865})
