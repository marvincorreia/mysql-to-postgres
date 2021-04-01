import os
import subprocess
from dotenv import load_dotenv
from inquirer2 import print_json
from operator import itemgetter

import utils.questions as Q
from utils.db.my_connector import MYConnector

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
    "Data and Structure": "",
}

operations = ["Make Dump", "Make Migration to postgres", "Exit"]

# mysql_dumps = {
#     "structure": f"mysqldump -u {} -p{} -h {} -P {} --databases {} --no-create-info --compact --compatible=ansi > data.sql"
#     "data": f"mysqldump -u {} -p{} -h {} -P {} --databases {} --no-create-info --compact --compatible=ansi > structure.sql"
# }

state = {
    'databases': [],
    'operation': "",
    'dump_mode': "",
    'config': {
        'port': "3306",
        'host': "127.0.0.1",
        'user': "root",
        "password": "",
        'raise_on_warnings': True
    },
    'cmd': ""
}


def nomalize(value, key=None):
    if key:
        return value.replace(" ", "_")
    else:
        return value.replace("_", " ")


def get_databases():
    conn = MYConnector(config=state['config'])
    if conn.connect():
        return [x[0] for x in conn.query("show databases;")]
        conn.close()
    return []


def generate_cmd():
    cmd = ""
    if state['operation'] == operations[0]:
        config, dump_mode = state['config'], dump_modes[state['dump_mode']]
        databases = " ".join(state['databases'])
        cmd = f"mysqldump -u {config['user']} -p{config['password']} -h {config['host']} -P {config['port']} \
        --databases {databases} {dump_mode} --compact --compatible=ansi > data.sql"
    state.update(dict(cmd=cmd))


def execute_cmd(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)


def menu_dump_mode():
    choices = list(dump_modes.keys())
    result = Q.list_input('dump_mode', "Which kind of dump", choices, sep_text="Select dump mode")
    state.update(result)


def menu_select_databases():
    choices = get_databases()
    result = Q.select_input("databases", "Select databases to dump", choices)
    if not result['databases']:
        print("\nERROR: You must select at least one database!\n")
        menu_select_databases()
    state.update(result)


def menu_db_creadentials():
    while True:
        config = state['config']
        result = Q.text_input("host", "MYSQL DB host", default=config['host'])
        result.update(Q.number_input("port", "MYSQL DB port", default=config['port']))
        result.update(Q.text_input("user", "MYSQL DB user", default=config['user']))
        result.update(Q.password_input("password", "MYSQL DB password"))
        state.update(dict(config=result))
        conn = MYConnector(config=state['config'])
        if conn.connect():
            conn.close()
            return True
        else:
            status = Q.confirm_input("continue", "Try again?", default=True)
            if not status['continue']:
                return False


def menu():
    while True:
        result = Q.list_input('operation', "Choise an operation", operations)
        state.update(result)
        if state['operation'] == operations[0]:
            if menu_db_creadentials():
                menu_select_databases()
                menu_dump_mode()
                generate_cmd()
            # execute_cmd(cmd)
        elif state['operation'] == operations[1]:
            continue
        else:
            break


if __name__ == '__main__':
    menu()
    print_json(state)
