from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from examples import custom_style_1
from examples import custom_style_3
import requests
import regex
from pprint import pprint
from urllib3.util import Url
from common.configurls import URLConfigs
import common
from situationalawareness.comprehensionstage import TCONST
import os
import json
import click

urls = URLConfigs(common.michost, common.gpshost, common.sahost) #will initialize correct values in main

def clearScreen():
    os.system('clear')
    os.system("printf '\e[3J'")

class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='DELETE YOUR RESPONSE AND ENTER A NUMBER',
                cursor_position=len(document.text))  # Move cursor to end

def getBrokenPolicyTrackers(policyid: str):
    path = "/getBrokenPolicyTrackers/"+policyid
    serviceURL = Url(scheme=urls.SA_HOST.scheme, host=urls.SA_HOST.host, port=urls.SA_HOST.port, path=path)
    data = callRestGet(serviceURL)
    trackers = data['trackers']
    return trackers

def getBrokenPolicies():
    path = "/getBrokenPolicies"
    serviceURL = Url(scheme=urls.SA_HOST.scheme, host=urls.SA_HOST.host, port=urls.SA_HOST.port, path=path)
    data = callRestGet(serviceURL)
    policies = data['policies']
    return policies

def getPolicies():
    path = "/getPolicies"
    serviceURL = Url(scheme=urls.SA_HOST.scheme, host=urls.SA_HOST.host, port=urls.SA_HOST.port, path=path)
    data = callRestGet(serviceURL)
    policies = data['policies']
    return policies

def getPolicy(op):
    policies = getPolicies()

    choices = []
    for policy in policies:
        choices.append(str(policy))

    data = {
        'type': 'list',
        'name': 'policy',
        'message': 'Available Policies: (select to '+op+')',
        'choices': choices
    }

    selection = prompt(data)
    out = eval(selection['policy'])
    return out

def getPolicyDetail(policyid: str):
    path="/getPolicy/"+policyid
    serviceURL = Url(scheme=urls.SA_HOST.scheme, host=urls.SA_HOST.host, port=urls.SA_HOST.port, path=path)
    data = callRestGet(serviceURL)
    return data['policy']

def getTracker(policyid: str):
    path="/getTracker/"+policyid
    serviceURL = Url(scheme=urls.SA_HOST.scheme, host=urls.SA_HOST.host, port=urls.SA_HOST.port, path=path)
    data = callRestGet(serviceURL)
    pprint(data)
    return data['tracker']

def callRestPost(serviceURL: Url, jsonData=None):
    print("Request: " + serviceURL.url)
    response = requests.post(serviceURL.url, json=jsonData)
    data = response.json()
    return data

def callRestGet(serviceURL: Url):
    print("Request: " + serviceURL.url)
    response = requests.get(serviceURL.url)
    data = response.json()
    return data

def brokenPolicies():
    try:
        loop = True
        while loop:
            policies = getBrokenPolicies()
            clearScreen()
            if(len(policies) > 0):
                choices = []
                for policy in policies:
                    choices.append(str(policy))

                data = {
                    'type': 'list',
                    'name': 'policy',
                    'message': 'Broken Policies: (select a policy to inspect its tracker instances)',
                    'choices': choices
                }

                selection = prompt(data)
                out = eval(selection['policy'])
                id = out[TCONST.ID]
                trackerStatus(id)

                loop = question('Find another broken policy?')
            else:
                pprint("No Broken Policies")
                loop = False

    except Exception:
        anyKey2Continue("The policy requested no longer exists.  You're likely seeing this message because someone has deleted it.")



def trackerStatus(id):
    try:
        loop = True
        while loop:
            clearScreen()
            trackers = getBrokenPolicyTrackers(id)
            pprint(trackers)
            loop = question('Refresh?')
    except Exception:
        anyKey2Continue("The policy being tracked no longer exists.  You're likely seeing this message because someone has deleted the policy")

def policyStatus():
    try:
        policy = getPolicy('query')

        loop = True
        while loop:
            tracker = getTracker(policy[TCONST.ID])
            clearScreen()

            if policy[TCONST.TYPE] == TCONST.TYPE_WIN:
                print(TCONST.ID+":\t\t", tracker[TCONST.ID])
                print(TCONST.COORD+":\t", tracker[TCONST.COORD])
                print(TCONST.NOISE_CUR+":\t", tracker[TCONST.NOISE_CUR])
                print(TCONST.NOISE_THRES+":\t", tracker[TCONST.NOISE_THRES])
                print(TCONST.NOISE_AVG+"\t", tracker[TCONST.NOISE_AVG])
                print(TCONST.WIN_SIZE+"\t", tracker[TCONST.WIN_SIZE])
                print(TCONST.TIME_START+"\t", tracker[TCONST.TIME_START])
                print(TCONST.TIME_END+"\t", tracker[TCONST.TIME_END])
                print(TCONST.TIME_CUR+"\t", tracker[TCONST.TIME_CUR])
            else:
                print(TCONST.ID+":\t\t", tracker[TCONST.ID])
                print(TCONST.COORD+":\t", tracker[TCONST.COORD])
                print(TCONST.NOISE_CUR+":\t", tracker[TCONST.NOISE_CUR])
                print(TCONST.NOISE_THRES+":\t", tracker[TCONST.NOISE_THRES])
                print(TCONST.NOISE_IMP+":\t", tracker[TCONST.NOISE_IMP])
                print(TCONST.TIME_IMP+":\t", tracker[TCONST.TIME_IMP])
                print(TCONST.TIME_CUR+":\t", tracker[TCONST.TIME_CUR])

            loop = question('Refresh?')
    except Exception:
        anyKey2Continue("The policy has either been deleted already or was invalid.")

def policyRemove():
    try:
        loop = True
        while loop:
            clearScreen()
            policy = getPolicy('remove')
            policyid = policy[TCONST.ID]

            path = "/removeWindowPolicy/" + policyid
            serviceURL = Url(scheme=urls.SA_HOST.scheme, host=urls.SA_HOST.host,
                             port=urls.SA_HOST.port, path=path)
            data = callRestGet(serviceURL)
            pprint(data)

            loop = question('Delete another policy?')
    except Exception:
        pass #if the policy you entered does not exist then bonus.. its deleted haha [thumbs up]

def createNumQuestion(tag, message):
    return {
        'type': 'input',
        'name': tag,
        'message': message,
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    }


def policyAdd():
    path = "/addWindowPolicy"
    serviceURL = Url(scheme=urls.SA_HOST.scheme, host=urls.SA_HOST.host,
                     port=urls.SA_HOST.port, path=path)

    questions = [
        createNumQuestion(TCONST.WIN_SIZE, 'Enter the '+TCONST.WIN_SIZE),
        createNumQuestion(TCONST.NOISE_THRES, 'Enter the ' + TCONST.NOISE_THRES)
    ]

    loop = True
    while loop:
        clearScreen()
        answers = prompt(questions, style=custom_style_3)
        jsonData = json.dumps(answers)
        data = callRestPost(serviceURL, jsonData)
        pprint("Policy Added:")
        pprint(data)
        loop = question('Add another policy?')



def performOperation():
    query = 'Query Policy'
    remove = 'Remove Policy'
    add = 'Add Policy'
    broken = 'List Broken Policies'
    choices = [query, remove, add, broken]

    data = {
        'type': 'list',
        'name': 'policy',
        'message': 'Select an operation to perform:)',
        'choices': choices
    }

    selection = prompt(data)
    out = selection['policy']
    if (out == query):
        policyStatus()
    elif (out == remove):
        policyRemove()
    elif (out == add):
        policyAdd()
    elif (out == broken):
        brokenPolicies()

def question(message):
    op = 'again'
    questions = [
        {
            'type': 'confirm',
            'message': message,
            'name': op,
            'default': False,
        }
    ]
    answers = prompt(questions, style=custom_style_1)
    return answers[op]

def anyKey2Continue(message):
    op = 'anykey'
    questions = [
        {
            'type': 'input',
            'name': op,
            'message': message+" Press return to continue.",
        }
    ]
    #simply block until anykey is entered
    prompt(questions, style=custom_style_1)

@click.command()
@click.option('--sahost', '-s', envvar="SAHOST")
def main(sahost):
    for param in os.environ.keys():
        if 'HOST' in param:
            print ("%20s %s" % (param, os.environ[param]))

    if(sahost is not None):
        common.sahost = sahost

    global urls
    urls = URLConfigs(common.michost, common.gpshost, common.sahost)
    click.echo("{}, {}, {}".format(sahost, common.sahost, urls.SA_HOST))

    loop = True
    while loop:
        clearScreen()
        performOperation()
        loop = question('Perform another operation?')

    pprint("Have a great day")

if __name__ == '__main__':
    main()


