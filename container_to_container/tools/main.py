import json
from flask import Flask, render_template, request, Response, send_from_directory, session
from io import BytesIO
from captcha.image import ImageCaptcha
import random
import base64
from process_emails import process_emails

container_name_mongo:str = "overleafmongo"
port_mongo: int = 27017
container_name_overleaf: str = "overleafserver"

app = Flask(__name__)

with open("secret_key.json", "r") as file:
    secret_key: dict = json.load(file)

assert secret_key is not None
assert secret_key["secret_key"] is not None
app.config['SECRET_KEY'] = secret_key["secret_key"]


def generate_captcha():
    image = ImageCaptcha(width=280, height=90)
    captcha_text = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    data = image.generate(captcha_text)
    return captcha_text, data

@app.route("/register", methods=["GET", "POST"])
def index() -> Response:

    if request.method == "GET":
        captcha_text, captcha_image = generate_captcha()
        session['captcha'] = captcha_text
        captcha_base64 = base64.b64encode(captcha_image.getvalue()).decode('utf-8')
        return render_template('post.html', captcha_image=captcha_base64)

    elif request.method == "POST":
        post_content = request.form.get('content')
        email = request.form.get('email')
        user_captcha = request.form.get('captcha')

        if user_captcha and user_captcha.upper() == session.get('captcha'):
            if process_emails(mail_address=email,container_name_mongo=container_name_mongo,port_mongo=port_mongo,container_name_overleaf=container_name_overleaf):
                return f"A email was sent to {email}. Please click the activation link. Please check your spam folder! <p> <a href='https://overleaf.neuro.uni-bremen.de/'>Back to the overleaf site...</a>"
            else:
                return f"We couldn't register your email {email}."
        else:
            return f"There was a problem with solving the captcha. Try again. Sorry!"

@app.route("/register/static/<path:path>", methods=["GET"])
def serve_static_files(path) -> Response:
    return send_from_directory("static", path)
