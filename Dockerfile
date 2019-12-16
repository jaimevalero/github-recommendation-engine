FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN  pip3.8 install -r /usr/src/app/requirements.txt
#CMD [ "python3.8", "./app.py" ]
CMD ["gunicorn"  , "-b", "0.0.0.0:80", "-w", "6", "app:app"]

