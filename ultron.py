from flask import Flask, render_template, request


application = Flask(__name__)


@application.route("/")
def homepage():
    return render_template('index.html')


@application.route("/", methods=['POST'])
def webhook():
    data = request.get_json()
    return "ok"


if __name__ == "__main__":
    application.run(host='0.0.0.0')
