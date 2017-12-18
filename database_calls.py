#! /usr/bin/env python3
import sqlite3
import sys

from generate_insert_statement import generate_insert

def load_data_into_table(db_name, table_name, data_list):
    '''
    
    '''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()    

    for record in data_list:
        sql_call = generate_insert(table_name, record)

        try:
            cursor.execute(sql_call)
        except:
            print(sys.exc_info())
            print(sql_call)
            break

    conn.commit()
    cursor.close()
    conn.close()


def create_database(db_name, table_name, attribute_dict, primary_key):
    '''
    Parameters:
        1. string database name
        2. string table name
        3. dictionary of table attributes
            'table': {
                0: {'column_name': 'ID', 'data_type': 'INTEGER'},
                1: {'column_name': 'backend', 'data_type': 'TEXT'},
                ...
            }

        4. string for primary key
           primary_key = 
              'CONSTRAINT transaction_pk
                   PRIMARY KEY (transaction_id, company_id),

               CONSTRAINT transactions_fk
                   FOREIGN KEY (company_id)
                       REFERENCES company(company_id)'

    Returns:
        - True if successful
        - False if not successful
    '''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    
    build_table_sql = 'CREATE TABLE {} (\n'.format(table_name)


    for key, value in attribute_dict.items():
        build_table_sql += "\t{} {},\n".format(value['name'], value['data_type'])

    build_table_sql += '\n\t{}\n);'.format(primary_key)
    
    try:
        cursor.execute(build_table_sql)
        flag = True
        print('{} database created.'.format(db_name))

    except:
        print(sys.exc_info())
        print(build_table_sql)
        flag = False

    finally:
        conn.commit()
        cursor.close()
        conn.close()

    return flag