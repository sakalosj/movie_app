FROM ubuntu

RUN apt-get update && apt-get install -y python3 python3-all python3-venv\
 python3-setuptools python3-pip vim git libpq-dev python-dev telnet tcpdump

WORKDIR /movie_app

COPY requirements* /movie_app/
RUN pip3 install virtualenv
RUN python3 -m venv venv


RUN ./venv/bin/pip3 install -U pip
RUN ./venv/bin/pip3 install -r requirements.txt

COPY . /movie_app
RUN ./venv/bin/pip3 install -e .


CMD ./venv/bin/gunicorn -w 4 -b 0.0.0.0:4000 movie_app.app:app

