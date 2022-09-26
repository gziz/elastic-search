FROM python:3.9

COPY ./requirements.txt /qa_proj/requirements.txt

WORKDIR /qa_proj
RUN python3 -m venv /opt/venv && /opt/venv/bin/python -m pip install -r requirements.txt

COPY ./app ./app
COPY ./entrypoint.sh ./entrypoint.sh

RUN chmod +x entrypoint.sh


CMD ["./entrypoint.sh"]