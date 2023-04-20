FROM python:3.10-buster

COPY . /root/projects/delivery

WORKDIR /root/projects/delivery

RUN pip install pipenv
RUN mkdir .venv
RUN pipenv install

ENV APP_CONFIG_FILE '/root/projects/delivery/config/production/config.py'

CMD /root/projects/delivery/.venv/bin/gunicorn --workers 2 --bind 0:5000 "app:create_app()"
