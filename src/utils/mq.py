from inquirer2 import prompt
from pprint import pprint

import validators
import style

def new_connection():
    questions = [
        {
            'type': 'input',
            'name': 'host',
            'message': 'Database Host:',
            'validate': validators.EmptyTextValidator
        }, {
            'type': 'input',
            'name': 'port',
            'message': 'Database Port',
            'validate': validators.NumberValidator
        }, {
            'type': 'input',
            'name': 'user',
            'message': 'Database User:',
            'validate': validators.EmptyTextValidator
        }, {
            'type': 'password',
            'message': 'Database Password:',
            'name': 'password'
        }
    ]

    answers = prompt.prompt(questions, style=style.custom_style_2)
    pprint(answers) 


new_connection()



