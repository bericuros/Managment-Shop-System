FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

COPY ./application.py ./application.py
COPY ./configuration.py ./configuration.py
COPY ./models.py ./models.py
COPY ./messages.py ./messages.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]
