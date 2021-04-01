# -*- coding: utf-8 -*-
"""
* Checkbox question example
* run example by typing `python example/checkbox.py` in your console
"""
from pprint import pprint
from inquirer2 import prompt, Separator
from . import style

from . import validators


mstyle = style.custom_style_2

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

q_confirm =[
     {
        'type': 'confirm',
        'message': 'Do you want to continue?',
        'name': 'continue',
        'default': True,
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
    answers = prompt.prompt(question, style=mstyle)
    return answers


def password_input(name, message=None):
    question = q_pwd.copy()
    if message:
        question[0]['message'] = message
    question[0]['name'] = name
    answers = prompt.prompt(question, style=mstyle)
    return answers


def text_input(name, message, empty=None, default=None):
    question = q_text.copy()
    if empty:
        del question[0]['validate']
    if default:
        question[0]['default'] = default
    question[0]['message'] = message
    question[0]['name'] = name
    return prompt.prompt(question, style=mstyle)


def number_input(name, message, empty=None, default=None):
    question = q_number.copy()
    question[0]['message'] = message
    question[0]['name'] = name
    if default:
        question[0]['default'] = default
    return prompt.prompt(question, style=mstyle)


def list_input(name, message, choices, sep_text=None):
    question = q_list_select.copy()
    m_choices = [Separator(f'\n== {sep_text} ==\n'), ] if sep_text else []
    for choice in choices:
        m_choices.append({'name': choice})

    question[0]['message'] = message
    question[0]['name'] = name
    question[0]['choices'] = m_choices
    answers = prompt.prompt(question, style=mstyle)
    return answers


def confirm_input(name, message, default=None):
    question = q_confirm.copy()
    question[0]['message'] = message
    question[0]['name'] = name
    if default != None:
        question[0]['default'] = default
    return prompt.prompt(question, style=mstyle)