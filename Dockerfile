FROM python:3.8.12

WORKDIR /usr/src/app

COPY . .
RUN  pip install -r /usr/src/app/requirements.txt
CMD ["gunicorn"  , "-b", "0.0.0.0:80", "-w", "4", "app:app" ]


