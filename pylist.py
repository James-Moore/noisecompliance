from pprint import pprint
from PyInquirer import prompt
from PyInquirer import Separator
from examples import custom_style_2

class PyList:
    def __init__(self):
        pass


    def get_delivery_options(answers):
        options = ['bike', 'car', 'truck']
        if answers['size'] == 'jumbo':
            options.append('helicopter')
        return options


    def execute(self):
        questions = [
            {
                'type': 'list',
                'name': 'theme',
                'message': 'What do you want to do?',
                'choices': [

                ]
            }
        ]

        answers = prompt(questions, style=custom_style_2)
        pprint(answers)


PyList().execute()