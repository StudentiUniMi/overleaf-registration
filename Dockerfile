FROM python:slim

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000
ENTRYPOINT ["/bin/bash", "-c", "gunicorn wsgi:app --bind 0.0.0.0:8000 --env CAPTCHA_CLIENT_KEY=$CAPTCHA_CLIENT_KEY --env CAPTCHA_SERVER_KEY=$CAPTCHA_SERVER_KEY --env OF_INSTANCE=$OF_INSTANCE --env OF_ADMIN_EMAIL=$OF_ADMIN_EMAIL --env OF_ADMIN_PASSWORD=$OF_ADMIN_PASSWORD"]
