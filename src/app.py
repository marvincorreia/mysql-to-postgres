import os
from dotenv import load_dotenv
import utils.questions as Q
from utils.db.my_connector import MYConnector
from inquirer2 import print_json

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '3306',
    #   'database': 'employees',
    'raise_on_warnings': True
}

skip_definer = " | sed -e 's/DEFINER[ ]*=[ ]*[^*]*\*/\*/' | sed -e 's/DEFINER[ ]*=[ ]*[^*]*PROCEDURE/PROCEDURE/' | sed -e 's/DEFINER[ ]*=[ ]*[^*]*FUNCTION/FUNCTION/' > dump.sql"

dump_modes = {
    "Only Data": "--no-create-info",
    "Only Structure": "--no-data",
    "Data and Structure": ""
}

operations = ["Make Dump", "Make Migration to postgres"]

mysql_dumps = {
    "structure": f"mysqldump -u {} -p{} -h {} -P {} --databases {} --no-create-info --compact --compatible=ansi > data.sql"
    "data": f"mysqldump -u {} -p{} -h {} -P {} --databases {} --no-create-info --compact --compatible=ansi > structure.sql"
}

all_info = {
    'databases': [],
    'operation': ""
    'dump_mode': ""
    'port': ""
    'host': ""
}


def nomalize(value, key=None):
    if key:
        return value.replace(" ", "_")
    else:
        return value.replace("_", " ")


def get_databases():
    conn = MYConnector(config=config)
    if conn.connect():
        return [x[0] for x in conn.query("show databases;")]
        conn.close()
    return []


def execute_cmd():
    cmd = f"mysqldump -u {} -p{} -h {} -P {} --databases {} --no-create-info --compact --compatible=ansi > data.sql"
    if all_info['operation'] == operations[0]:


def menu_dump_mode():
    choices = list(dump_modes.keys())
    result = Q.list_input('dump_mode', "Which kind of dump", choices, sep_text="Select dump mode")
    all_info.update(result)


def menu_select_databases():
    choices = get_databases()
    result = Q.select_input("databases", "Select databases to dump", choices)
    if not result['databases']:
        print("\nERROR: You must select at least one database!\n")
        menu_select_databases()
    all_info.update(result)


# def menu_db_creadentials():
#     result = Q.


def menu():
    result = Q.list_input('operation', "Choise an operation", operations)
    all_info.update(result)
    if all_info['operation'] == operations[0]:
        menu_select_databases()
        menu_dump_mode()
    else:
        return


if __name__ == '__main__':
    # print(dbs)
    menu()
    print_json(all_info)
