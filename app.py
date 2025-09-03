from flask import Flask, render_template, request, jsonify, render_template_string, send_from_directory

import requests
import hashlib
import hjson
import time
import os

app = Flask(__name__)

languageForUser = {}

templates = {}
variables = {}
online = {}

now = {}

log = ""


def write(*args):
    global log

    log += f"{' '.join([str(element) for element in args])}\n"

    print(f"{' '.join([str(element) for element in args])}")


def initialization(ip):
    # DOWNLOAD VARIABLES

    url = "https://raw.githubusercontent.com/artyom7774/Game-Engine-3/main/scr/files/version.json"

    try:
        response = requests.get(url)
        data = response.json()

        variables["GE3Version"] = data["version"]

    except Exception:
        variables["GE3Version"] = "0"

    url = "https://raw.githubusercontent.com/artyom7774/GELauncher/main/scr/files/version.json"

    try:
        response = requests.get(url)
        data = response.json()

        variables["GELauncherVersion"] = data["version"]

    except Exception:
        variables["GELauncherVersion"] = "0"

    url = "https://raw.githubusercontent.com/artyom7774/Game-Engine-3/main/scr/files/updates.json"

    try:
        response = requests.get(url)
        data = response.json()

        variables["updates"] = data

    except Exception:
        variables["updates"] = None

    with open("base/scr/header.html", "r", encoding="utf-8") as file:
        variables["HEADER"] = file.read()

    with open("base/scr/footer.html", "r", encoding="utf-8") as file:
        variables["FOOTER"] = file.read()

    variables["online"] = len(online)

    # CREATE UPDATES MENU

    updates = ""

    if variables["updates"] is not None:
        for update in variables["updates"]["sorted"][::-1]:
            updates += "<div class='main__updates__element'>"

            version = variables['updates']['updates'][update]

            updates += f"<p class='main__updates__element__title'>Game Engine {version['name']}</p>"

            updates += "<div class='main__updates__element__list'>"

            text = version["text"]

            out = ""

            flag = False

            for symbol in text:
                if symbol == "-":
                    if flag:
                        out += "<br>-"

                    else:
                        flag = True

                        out += "-"

                else:
                    out += symbol

            updates += out

            updates += "</div>"

            updates += "</div>"

    variables["UPDATES"] = updates

    init(ip, languageForUser.get(ip, "en"))


def init(ip, language):
    # CREATE TEMPLATES FILES & TRANSLATING

    templates[ip] = {}

    for root, dirs, files in os.walk("base"):
        for pathfile in files:
            path = f"{root}/{pathfile}"

            if pathfile.endswith(".py"):
                continue

            with open(path, "r", encoding="utf-8") as file:
                text = file.read()

            for key, value in variables.items():
                while text.find(f"${key}$") != -1:
                    text = text.replace(f"${key}$", str(value))

            with open(f"bundles/{language}.hjson", "r", encoding="utf-8") as file:
                bundle = hjson.load(file)

            for key, value in bundle.items():
                while text.find(f"&{key}&") != -1:
                    text = text.replace(f"&{key}&", value)

            templates[ip][pathfile] = text


def start():
    write("-------------------- LOG --------------------")

    app.run(debug=True, use_reloader=False)

    app.config["UPLOAD_FOLDER"] = "scr"
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 ** 2


@app.before_request
def flask():
    if hashlib.sha256(request.remote_addr.encode()).hexdigest() not in templates:
        initialization(hashlib.sha256(request.remote_addr.encode()).hexdigest())


@app.route("/")
def index():
    global now

    ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()

    now[ip] = "index.html"

    deleteFromOnlineList()
    initialization(ip)

    return render_template_string(templates[ip][now[ip]])


@app.route("/download/")
def download():
    global now

    ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()

    now[ip] = "download.html"

    deleteFromOnlineList()
    initialization(ip)

    return render_template_string(templates[ip][now[ip]])


@app.route("/community/")
def community():
    global now

    ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()

    now[ip] = "community.html"

    deleteFromOnlineList()
    initialization(ip)

    return render_template_string(templates[ip][now[ip]])


@app.route("/updates/")
def updates():
    global now

    ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()

    now[ip] = "updates.html"

    deleteFromOnlineList()
    initialization(ip)

    return render_template_string(templates[ip][now[ip]])


@app.route("/documentation/")
def documentation():
    global now

    ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()

    now[ip] = "documentation.html"

    deleteFromOnlineList()
    initialization(ip)

    return render_template_string(templates[ip][now[ip]])


@app.route("/documentation/nodes")
def nodes():
    global now

    ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()

    now[ip] = "nodes.html"

    deleteFromOnlineList()
    initialization(ip)

    return render_template_string(templates[ip][now[ip]])


@app.route("/documentation/first-program")
def first_program():
    global now

    ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()

    now[ip] = "first-program.html"

    deleteFromOnlineList()
    initialization(ip)

    return render_template_string(templates[ip][now[ip]])


@app.route("/documentation/variables")
def _variables():
    global now

    ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()

    now[ip] = "variables.html"

    deleteFromOnlineList()
    initialization(ip)

    return render_template_string(templates[ip][now[ip]])


@app.route("/documentation/programming")
def programming():
    global now

    ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()

    now[ip] = "programming.html"

    deleteFromOnlineList()
    initialization(ip)

    return render_template_string(templates[ip][now[ip]])


@app.route("/log")
def _log():
    global log

    text = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Game Engine 3</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
        <link rel="icon" href="{{ url_for('static', filename='images/logo/dark.png') }}" type="image/x-icon">
    </head>
    <body>
        <style>
          pre {
            color: #FFFFFF;
          }
        </style>
        <pre>{{ log }}</pre>
        <script src="{{ url_for('static', filename='js/code.js') }}"></script>
        <script data-goatcounter="https://artyom7777.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
    </body>
    </html>
    """

    return render_template_string(text, log=log)


@app.route("/setLanguage", methods=["POST"])
def setLanguage():
    global now

    ip = hashlib.sha256(request.remote_addr.encode()).hexdigest()

    if ip not in now:
        now[ip] = "index.html"

    languageForUser[ip] = request.form.get("id")

    init(ip, request.form.get("id"))

    return jsonify({"text": render_template_string(templates[ip][now[ip]])})


@app.route("/updateOnline", methods=["POST"])
def updateOnline():
    ip = request.form.get("ip")

    online[ip] = {
        "time": time.time()
    }

    return jsonify({"status": "success"}), 200


def deleteFromOnlineList():
    global online

    with app.app_context():
        rem = []

        for ip, user in online.items():
            write(ip, time.time() - user["time"])

            if time.time() - user["time"] >= 150:
                rem.append(ip)

        for element in rem:
            if element in online:
                del online[element]

        write(len(online), online)


@app.route("/scr/<path:filename>")
def image(filename):
    return send_from_directory("scr", filename)


if __name__ == "__main__":
    start()
