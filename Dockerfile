FROM python:3.9

WORKDIR /qa_proj
COPY ./requirements.txt ./requirements.txt

RUN python3 -m venv /opt/venv && /opt/venv/bin/python -m pip install -r requirements.txt

COPY .env ./.env
COPY ./pipelines ./pipelines
RUN /opt/venv/bin/python -m pypyr pipelines/model-download
RUN /opt/venv/bin/python -m pypyr pipelines/haystack-model-download

COPY ./app ./app
COPY ./entrypoint.sh ./entrypoint.sh

RUN chmod +x entrypoint.sh


CMD ["./entrypoint.sh"]
