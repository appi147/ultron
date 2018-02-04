from flask import Flask, render_template, request
import requests
import apiai


API_ACCESS_TOKEN = '6b19097281d4497f8126c12c9f7146a0'
WIT_TOKEN = 'LNXRDEZGL53OOPT6JH7QSC7H5QJUYGNB'
WIT_URL = 'https://api.wit.ai/message?v=04/02/2018&q='
application = Flask(__name__)
ai = apiai.ApiAI(API_ACCESS_TOKEN)


@application.route("/", methods=['GET'])
def homepage():
    query = request.args.get('query')
    if query is None:
        return render_template('index.html')
    else:
        return "pass"


def execute(query):
    pass


def handler(query):
    inp, resp = dialogflow(query)
    entities = wit(query)
    if inp is not None:
        return 'api', resp
    if inp is None:
        if 'action' in entities and 'act' in entities:
            action = entities['action'][0]['value']
            act = entities['act'][0]['value']
            return 'wit', action, act
        else:
            return 'api', resp
    return 'fail'


def wit(query):
    headers = {'Authorization': 'Bearer ' + WIT_TOKEN}
    try:
        r = requests.get(url=WIT_URL+query, headers=headers)
    except Exception as e:
        print('Exception ' + e)
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
        inp = dt['result']['action']
        if inp == 'input.unknown':
            inp = None
    except Exception as e:
        print('Exception ' + e)
        return None, None
    return inp, resp


if __name__ == "__main__":
    application.run(host='0.0.0.0')
