from flask import Flask, render_template, request, jsonify, render_template_string, send_from_directory

import requests
import json

app = Flask(__name__)

content = ""

language = "en"
menu = "Game Engine 3"

menues = {
    "Game Engine 3": {

    },

    "Download": {

    },

    "Control": {

    },

    "Nodes": {

    },

    "Guides": {

    },

    "Programming": {

    }
}

translates = {
    "en": json.load(open("bundles/en.json", encoding="utf-8")),
    "ru": json.load(open("bundles/ru.json", encoding="utf-8"))
}


def decodeText(var):
    text = ""

    for line in var:
        if line == "-" * 100:
            line = "<br>"

        if line == "":
            line = "<br>"

        if line[0] == "<" and line[-1] == ">":
            text += line

        else:
            text += f"<p class='content__main__discription'>{line}</p>"

    return handleText(text)


def handleText(text):
    try:
        response = requests.get("https://raw.githubusercontent.com/artyom7774/Game-Engine-3/main/scr/files/version.json")
        data = response.json()
        version = data.get("version", "unknown")

    except Exception as e:
        print(f"ERROR: {e}")

        return text

    while text.find("%version%") != -1:
        text = text.replace("%version%", version)

    return text


def createContent():
    global content, language, menu

    out = "<div class='content__menu__choose'>"

    for key in menues.keys():
        out += f"<button class='content__menu__button' onclick='clickHandler(\"{key}\")'>&nbsp;{translates[language][key]['name']}</button>"

        for i, element in enumerate(menues[key].keys()):
            name = f"{key}/{element}"

            out += f"<button class='content__menu__button' onclick='clickHandler(\"{key}/{element}\")'>&nbsp;{translates[language][name]['name']}</button>"

    out += "</div>"

    language_settings = f"""
    <div class='content__menu__separator'></div>
    <div class='content__menu__settings'>
        <p class='settings__title'>{'Language Settings' if language == 'en' else 'Настройки языка'}</p>
        <button class='language__button' onclick='changeLanguage("en")'>English</button>
        <button class='language__button' onclick='changeLanguage("ru")'>Русский</button>
    </div>
    """

    content = f"""
    <header class="header">
        <p class="header__name">Game Engine 3</p>
        <p class="header__discription">{translates[language]["__desctiption__"]["text"]}</p>
    </header>

    <content class="content">
        <div class="content__menu">{out}{language_settings}</div>
        <div class="content__main">{decodeText(translates[language][menu]["text"])}</div>
    </content>

    <footer class="footer">
        <p class="footer__text">Game Engine 3 ©2024-2025</p>
    </footer>
    """

    return content


def start():
    content = createContent()

    html = open("template.html", "r", encoding="utf-8").read()
    html = html.replace("&{MAIN}&", f"<div class='main'>{content}</div>")

    with open("templates/index.html", "w", encoding="utf-8") as file:
        file.write(html)

    app.run(debug=True)

    app.config["UPLOAD_FOLDER"] = "scr"
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 ** 2


@app.route("/")
def index():
    return render_template("index.html", content=content)


@app.route("/scr/<path:filename>")
def image(filename):
    return send_from_directory("scr", filename)


@app.route("/click", methods=["POST"])
def click():
    global content, menu, language

    id = request.form.get("id")

    if not translates[language][id].get("visible", True) or id not in list(menues.keys()):
        return None

    menu = id

    content = createContent()

    response = {
        "status": "success",
        "button_id": id,
        "body": render_template_string(content)
    }

    return jsonify(response)


@app.route("/setLanguage", methods=["POST"])
def setLanguage():
    global content, menu, language

    language = request.form.get("id")

    content = createContent()

    response = {
        "status": "success",
        "body": render_template_string(content)
    }

    return jsonify(response)


if __name__ == "__main__":
    start()
