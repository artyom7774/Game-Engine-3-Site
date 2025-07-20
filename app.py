from flask import Flask, render_template, request, jsonify, render_template_string, send_from_directory

import requests
import hjson
import os

app = Flask(__name__)

variables = {}
language = "en"

now = "index.html"


def initialization():
    # DOWNLOAD VARIABLES

    url = "https://raw.githubusercontent.com/artyom7774/Game-Engine-3/main/scr/files/version.json"

    try:
        response = requests.get(url)
        data = response.json()

        variables["GE3Version"] = data["version"]

    except Exception:
        variables["GE3Version"] = "3.12.1"

    url = "https://raw.githubusercontent.com/artyom7774/GELauncher/main/scr/files/version.json"

    try:
        response = requests.get(url)
        data = response.json()

        variables["GELauncherVersion"] = data["version"]

    except Exception:
        variables["GELauncherVersion"] = "1.0.0"

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

    # CREATE UPDATES MENU

    updates = ""

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

    print(variables)

    init()


def init():
    # CREATE TEMPLATES FILES & TRANSLATING

    for root, dirs, files in os.walk("base"):
        for pathfile in files:
            path = f"{root}/{pathfile}"

            with open(path, "r", encoding="utf-8") as file:
                text = file.read()

            for key, value in variables.items():
                while text.find(f"${key}$") != -1:
                    text = text.replace(f"${key}$", value)

            with open(f"bundles/{language}.hjson", "r", encoding="utf-8") as file:
                bundle = hjson.load(file)

            for key, value in bundle.items():
                while text.find(f"&{key}&") != -1:
                    text = text.replace(f"&{key}&", value)

            with open(f"templates/{pathfile}", "w", encoding="utf-8") as file:
                file.write(text)


def start():
    initialization()

    app.run(debug=True)

    app.config["UPLOAD_FOLDER"] = "scr"
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 ** 2


@app.route("/")
def index():
    global now

    now = "index.html"

    return render_template(now)


@app.route("/download/")
def download():
    global now

    now = "download.html"

    return render_template(now)


@app.route("/community/")
def community():
    global now

    now = "community.html"

    return render_template(now)


@app.route("/updates/")
def updates():
    global now

    now = "updates.html"

    return render_template(now)


@app.route("/documentation/")
def documentation():
    global now

    now = "documentation.html"

    return render_template(now)


@app.route("/documentation/nodes")
def nodes():
    global now

    now = "nodes.html"

    return render_template(now)


@app.route("/documentation/first-program")
def first_program():
    global now

    now = "first-program.html"

    return render_template(now)


@app.route("/setLanguage", methods=["POST"])
def setLanguage():
    global language

    language = request.form.get("id")

    init()

    return jsonify({"text": render_template(now)})


@app.route("/scr/<path:filename>")
def image(filename):
    return send_from_directory("scr", filename)


if __name__ == "__main__":
    start()
