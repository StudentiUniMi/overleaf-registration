import re
import os

import requests
from flask import Flask, render_template, Response, request, send_from_directory

import overleaf

app = Flask(__name__)


def _check_captcha(code: str) -> bool:
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        "secret": os.environ.get("CAPTCHA_SERVER_KEY"),
        "response": code,
    })
    return r.json()["success"]


def _check_email(email: str) -> bool:
    return bool(re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email))


@app.route("/register", methods=["GET", "POST"])
def index() -> Response:
    if request.method == "GET":
        return render_template("register.html", CAPTCHA_CLIENT_KEY=os.environ.get("CAPTCHA_CLIENT_KEY"))

    elif request.method == "POST":
        captcha_code: str = request.form.get("g-recaptcha-response")
        if not _check_captcha(captcha_code):
            return render_template("error.html", error="Invalid CAPTCHA"), 403

        email: str = request.form.get("email")
        if not _check_email(email):
            return render_template("error.html", error="Invalid email"), 400

        ol = overleaf.Overleaf(os.environ.get("OL_INSTANCE"))
        ol.login(os.environ.get("OL_ADMIN_EMAIL"), os.environ.get("OL_ADMIN_PASSWORD"))
        ol.register_user(email)
        ol.logout()
        return render_template("done.html", submitted_email=email)


@app.route("/register/static/<path:path>", methods=["GET"])
def serve_static_files(path) -> Response:
    return send_from_directory("static", path)
