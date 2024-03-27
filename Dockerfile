FROM python:latest
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
CMD [ "python", "/app/main.py" ]
