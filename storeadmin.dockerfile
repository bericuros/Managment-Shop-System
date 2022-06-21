FROM python:3

RUN mkdir -p /opt/src/store
WORKDIR /opt/src/store

COPY store/admin/application.py ./admin.py
COPY store/configurationDatabase.py ./configurationDatabase.py
COPY store/models.py ./models.py
COPY messages.py ./messages.py
COPY check.py ./check.py
COPY store/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./admin.py"]
