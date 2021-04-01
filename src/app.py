import os
import subprocess
from dotenv import load_dotenv
from inquirer2 import print_json
from operator import itemgetter
import shlex
import re

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

# skip_definer = "sed -i 's/DEFINER[ ]*=[ ]*[^*]*\*/\*/' | sed -i 's/DEFINER[ ]*=[ ]*[^*]*PROCEDURE/PROCEDURE/' | sed -i 's/DEFINER[ ]*=[ ]*[^*]*FUNCTION/FUNCTION/'"

skip_definer = [
    's/DEFINER[ ]*=[ ]*[^*]*\*/\*/',
    's/DEFINER[ ]*=[ ]*[^*]*PROCEDURE/PROCEDURE/',
    's/DEFINER[ ]*=[ ]*[^*]*FUNCTION/FUNCTION/'
]

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


def try_again():
    status = Q.confirm_input("continue", "Try again?", default=True)
    return status['continue']


def generate_cmd():
    cmd = ""
    if state['operation'] == operations[0]:
        config, dump_mode = state['config'], dump_modes[state['dump_mode']]
        databases = " ".join(state['databases'])
        cmd = f"mysqldump -u {config['user']} -p{config['password']} -h {config['host']} -P {config['port']} \
        --databases {databases} {dump_mode} --set-charset=FALSE --compatible=ansi"
    state.update(dict(cmd=cmd))


def execute_cmd():
    generate_cmd()
    cmd = state['cmd'].split()
    sp = subprocess.run(cmd, shell=False, capture_output=True, text=True, cwd=os.path.dirname(__file__))
    stdout = sp.stdout
    for pattern in skip_definer:
        stdout = re.sub(pattern, '', stdout)
    with open(os.path.join(os.path.dirname(__file__), 'dump.sql'), mode='w') as fp:
        fp.write(stdout)


def menu_dump_mode():
    choices = list(dump_modes.keys())
    result = Q.list_input('dump_mode', "Select kind of dump", choices, sep_text="Select dump mode")
    state.update(result)


def menu_select_databases():
    choices = get_databases()
    while True:
        result = Q.select_input("databases", "Select databases to dump", choices)
        if not result['databases']:
            print("\nERROR: You must select at least one database!\n")
            continue
        state.update(result)
        break


def menu_db_connect():
    while True:
        config = state['config']
        result = Q.text_input("host", "DB HOST:", default=config['host'])
        result.update(Q.number_input("port", "DB PORT:", default=config['port']))
        result.update(Q.text_input("user", "DB USER:", default=config['user']))
        result.update(Q.password_input("password", "DB PASSWORD:"))
        state.update(dict(config=result))
        conn = MYConnector(config=state['config'])
        if conn.connect():
            conn.close()
            return True
        else:
            if not try_again():
                return False


def menu():
    while True:
        result = Q.list_input('operation', "Choise an operation", operations)
        state.update(result)
        if state['operation'] == operations[0]:
            if menu_db_connect():
                menu_select_databases()
                menu_dump_mode()
                execute_cmd()
        elif state['operation'] == operations[1]:
            continue
        else:
            break


if __name__ == '__main__':
    menu()
    print_json(state)
