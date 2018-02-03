from flask import Flask, render_template, request
import apiai


ACCESS_TOKEN = '6b19097281d4497f8126c12c9f7146a0'
application = Flask(__name__)
ai = apiai.ApiAI(ACCESS_TOKEN)


@application.route("/", methods=['GET'])
def homepage():
    query = request.args.get('query')
    if query is None:
        return render_template('index.html')
    else:
        return "ok"


def execute(query):
    pass


def dialogflow(query):
    resp = []
    request = ai.text_request()
    request.lang = 'en'
    request.session_id = "pi"
    request.query = query
    response = request.getresponse()
    a = response.read()
    dt = json.loads(a)
    try:
        resp.append(dt['result']['fulfillment']['speech'])
    except Exception as e:
        print('Exception ' + e)
    return resp


if __name__ == "__main__":
    application.run(host='0.0.0.0')
