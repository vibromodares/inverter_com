import numpy as np
import pandas as pd
from app.database.model.database_model import DataBaseModel
from tqdm import tqdm

database_db_path = './files/data/'
database_file_name = 'database.json'

import os


def make_tinydb_from_excel():
    # TODO:y dokme mikhaim k .json ro pak kone v jadid besaze v y ui mikhaim vase editesh
    df = pd.read_excel('files/data/iG5A_data.xlsx')

    if df['parent_id'].isnull().values.any():
        print('some parent id is nan')

    if df['address'].isnull().values.any():
        print('some Address is nan')

    if df['parameter'].isnull().values.any():
        print('some Parameter is nan')

    df['allotment_for_bits'] = df['allotment_for_bits'].fillna(value='')

    if df['description'].isnull().values.any():
        print('some description is nan')

    df['scale'] = df['scale'].fillna(value=-1)
    df['unit'] = df['unit'].fillna(value='')

    if df['RW'].isnull().values.any():
        print('some RW is nan')

    # df['decode_method'] = df['decode_method'].fillna(value=0)

    # df['range'] = df['range'].fillna(value='000F')
    if df['range'].isnull().values.any():
        print('some range is nan')

    for range in df['range']:
        if len(str(range)) != 4:
            print('range has wronged length')
            print(range)
            return

    df['important'] = df['important'].fillna(value=0)
    df['show'] = df['show'].fillna(value=0)
    df['need_update'] = df['need_update'].fillna(value=0)

    df['min'] = df['min'].fillna(value=0)
    df['max'] = df['max'].fillna(value=0)
    df['step'] = df['step'].fillna(value=-1)
    df['decimal'] = df['decimal'].fillna(value=-1)

    df['function'] = df['function'].fillna(value='')

    # print(df)

    if df.isnull().values.any():
        print('something is nan')
        return

    total_row = df.shape[0]

    database_table_name = 'iG5A'

    db = DataBaseModel(database_db_path, database_file_name, database_table_name)
    db.drop_all_data()

    with tqdm(total=total_row, desc=database_table_name) as pbar:
        for row in df.iterrows():
            pbar.update(1)
            temp_row = row[1]
            data = {
                'parent_id': int(temp_row['parent_id']),
                'address': str(temp_row['address']),
                'parameter': str(temp_row['parameter']),
                'allotment_for_bits': str(temp_row['allotment_for_bits']),
                'description': str(temp_row['description']),
                'scale': float(temp_row['scale']),
                'unit': str(temp_row['unit']),
                'RW': str(temp_row['RW']),
                # 'decode_method': temp_row['decode_method'],
                'range': str(temp_row['range']),
                'important': int(temp_row['important']),
                'show': int(temp_row['show']),
                'need_update': int(temp_row['need_update']),
                'min': int(temp_row['min']),
                'max': int(temp_row['max']),
                'step': int(temp_row['step']),
                'decimal': int(temp_row['decimal']),
                'function': str(temp_row['function']),

            }

            db.insert_data(data)

    # print(db)
    # db.insert_data({
    #     'parameter_name': 'Inverter Model',
    #     'address': '0x0300',
    #     'byte': '0x000A',
    #     'discreption': 'iG5A',
    # })


def check_db_exist() -> bool:
    return os.path.exists(database_db_path + database_file_name)


def handle_db() -> None:
    if not check_db_exist():
        make_tinydb_from_excel()
