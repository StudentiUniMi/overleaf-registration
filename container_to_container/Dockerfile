FROM python:3.12.4

RUN apt-get update 
RUN apt -y install mc
RUN apt -y install docker.io
RUN pip install pymongo
RUN pip install email_validator
RUN pip install flask
RUN pip install gunicorn
RUN pip install requests
RUN pip install BeautifulSoup4
RUN apt -y install bash
RUN pip install --upgrade pip
RUN pip install flask_wtf
RUN pip install wtforms
RUN pip install flask_recaptcha
RUN pip install Markup
RUN pip install captcha Pillow

COPY tools .

EXPOSE 80

ENTRYPOINT ["/bin/bash", "-c", "gunicorn wsgi:app --bind 0.0.0.0:80"]


