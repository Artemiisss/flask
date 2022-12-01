import datetime
import string
import random
from flask import Flask, request, render_template
from ua_parser import user_agent_parser

app = Flask(__name__)


@app.route("/")
def main():
    return "<h1>U are on the main page</h1>" \
           "<br>Enter  '/whoami'  to verify ur browser,ip and local time" \
           "<br>Enter  '/source_code'  to open an app in html" \
           "<br>Enter  '/random?length=42&specials=0&digits=0'  to create string of length count" \
           "<br>Enter  'specials=1'  into the link to create string with specials symbols" \
           "<br>Enter  'digits=1'  to create string with digits"


@app.route("/whoami")
def index():
    ip_address = request.remote_addr
    browser = user_agent_parser.Parse(request.user_agent.string)['user_agent']['family']
    dt = datetime.datetime.now()
    dt = dt.strftime("%H:%M:%S")
    return f"Requester IP: {ip_address}" \
           f"<br>Your time now is: {dt}" \
           f"<br>Your browser is: {browser}"


@app.route("/source_code")
def source_code():
    with open("main.py", 'r') as file:
        return render_template("index.html", text=file.read())


@app.route('/random', methods=['GET', 'POST'])
def random_string():
    length = request.args.get('length', type=int)
    specials = request.args.get('specials', type=int)
    digits = request.args.get('digits', type=int)

    if length in range(1, 100) and specials == 1 and digits == 1:
        letters = ''.join(random.choice(string.ascii_lowercase + string.digits + string.punctuation)
                          for _ in range(length))
        return letters

    if length in range(1, 100) and digits == 1:
        letters = ''.join(random.choice(string.ascii_lowercase + string.digits)
                          for _ in range(length))
        return letters

    if length in range(1, 100) and specials == 1:
        letters = ''.join(random.choice(string.ascii_lowercase + string.punctuation)
                          for _ in range(length))
        return letters

    if length in range(1, 100):
        letters = ''.join(random.choice(string.ascii_lowercase)
                          for _ in range(length))
        return letters

    else:
        return "Something went wrong, check the spelling"


if __name__ == '__main__':
    app.run(debug=True)
