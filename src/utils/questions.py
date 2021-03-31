# -*- coding: utf-8 -*-
"""
* Checkbox question example
* run example by typing `python example/checkbox.py` in your console
"""
from pprint import pprint
from inquirer2 import prompt, Separator
from . import style

from . import validators

q_select = [
    {
        'type': 'checkbox',
        'qmark': '?',
        'message': 'Select Databases to migrate to postgres',
        'name': 'selections',
        'choices': [
            Separator('= Databases on {host} ='),
            {
                'name': 'Ham',
                'checked': True
            },
            {
                'name': 'Ground Meat',
                'checked': False
            },
            {
                'name': 'Bacon',
                'checked': False
            }
        ],
        'validate': validators.EmptyTextValidator
    }
]

q_pwd = [
    {
        'type': 'password',
        'message': 'Enter your password',
        'name': 'password'
    }
]

q_text = [
    {
        'type': 'input',
        'name': 'text',
        'message': 'What\'s your first name',
        'validate': validators.EmptyTextValidator
    }
]

q_number = [
    {
        'type': 'input',
        'name': 'number',
        'message': 'Insert a number',
        'validate': validators.NumberValidator
    }
]

q_list_select = [
    {
        'type': 'list',
        'name': 'selected',
        'message': 'What do you want to do?',
        'choices': [
            'Order a pizza', 'Make a reservation',
            Separator(), 'Ask for opening hours', {
                'name': 'Contact support',
                'disabled': 'Unavailable at this time'
            }, 'Talk to the receptionist'
        ]
    }
]


def select_input(name, message, choices, sep_text=None):
    question = q_select.copy()
    m_choices = [Separator(f'\n== {sep_text} ==\n'), ] if sep_text else []
    for choice in choices:
        m_choices.append({'name': choice})

    question[0]['message'] = message
    question[0]['name'] = name
    question[0]['choices'] = m_choices
    answers = prompt.prompt(question, style=style.custom_style_3)
    return answers


def password_input(message=None):
    question = q_pwd.copy()
    if message:
        question[0]['message'] = message

    answers = prompt.prompt(question, style=style.custom_style_3)
    return answers


def text_input(message, empty=None):
    question = q_text.copy()
    if empty:
        del question[0]['validate']
    question[0]['message'] = message
    return prompt.prompt(question, style=style.custom_style_3)


def number_input(message):
    question = q_number.copy()
    question[0]['message'] = message
    return prompt.prompt(question, style=style.custom_style_3)


def number_input(message, empty=None):
    question = q_number.copy()
    question[0]['message'] = message
    return prompt.prompt(question, style=style.custom_style_3)


def list_input(name, message, choices, sep_text=None):
    question = q_list_select.copy()
    m_choices = [Separator(f'\n== {sep_text} ==\n'), ] if sep_text else []
    for choice in choices:
        m_choices.append({'name': choice})

    question[0]['message'] = message
    question[0]['name'] = name
    question[0]['choices'] = m_choices
    answers = prompt.prompt(question, style=style.custom_style_3)
    return answers
