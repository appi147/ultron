from flask import Flask, render_template, request
import requests
import apiai
import json


API_ACCESS_TOKEN = '6b19097281d4497f8126c12c9f7146a0'
WIT_TOKEN = 'LNXRDEZGL53OOPT6JH7QSC7H5QJUYGNB'
WIT_URL = 'https://api.wit.ai/message?v=04/02/2018&q='
application = Flask(__name__)
ai = apiai.ApiAI(API_ACCESS_TOKEN)


@application.route("/", methods=['GET', 'POST'])
def homepage():
    query = request.args.get('query')
    if query is None:
        return render_template('index.html')
    else:
        return execute(query)


def execute(query):
    state, first, second = handler(query)
    print(state, first, second)
    if state == 'api':
        return first
    if state == 'wit':
        return wit_handler(first, second)
    return 'fail'


def wit_handler(action, act):
    if action == 'turn on' and act == 'lights':
        return 'q1w2e3 on light'
    if action == 'turn off' and act == 'lights':
        return 'q1w2e3 off light'


def handler(query):
    inp, resp = dialogflow(query)
    entities = wit(query)
    print('Entities')
    print(entities)
    if inp is not None:
        return 'api', resp, 'api_found'
    if inp is None:
        if 'action' in entities:
            print('Action found')
        if 'act' in entities:
            print('Act found')
        if 'action' in entities and 'act' in entities:
            action = entities['action'][0]['value']
            act = entities['act'][0]['value']
            print('Action: '+action)
            print('Act: '+act)
            return 'wit', action, act
        else:
            return 'api', resp, 'api_no_match_wit_no_match'
    return 'fail', 'fake', 'fake'


def wit(query):
    headers = {'Authorization': 'Bearer ' + WIT_TOKEN}
    try:
        r = requests.get(url=WIT_URL+query, headers=headers)
    except Exception as e:
        print('Exception ' + str(e))
        return None
    return r.json()['entities']


def dialogflow(query):
    request = ai.text_request()
    request.lang = 'en'
    request.session_id = "pi"
    request.query = query
    response = request.getresponse()
    a = response.read()
    dt = json.loads(a)
    try:
        resp = dt['result']['fulfillment']['speech']
        try:
            inp = dt['result']['action']
        except Exception as e:
            print('Exception in dialogflow ' + str(e))
            inp = None
        if inp == 'input.unknown':
            inp = None
    except Exception as e:
        print('Exception in api server' + str(e))
        return None, None
    return inp, resp


if __name__ == "__main__":
    application.run(host='0.0.0.0')
