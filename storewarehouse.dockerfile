FROM python:3

RUN mkdir -p /opt/src/store
WORKDIR /opt/src/store

COPY store/warehouse/application.py ./warehouse.py
COPY store/configurationRedis.py ./configurationRedis.py
COPY store/models.py ./models.py
COPY messages.py ./messages.py
COPY check.py ./check.py
COPY store/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./warehouse.py"]
