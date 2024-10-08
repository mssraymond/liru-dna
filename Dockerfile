FROM python:3.11.9

WORKDIR /app

ENV PYTHONPATH="/app"

COPY src src/
COPY requirements.txt .
COPY secrets.yml .
COPY test.py .
COPY pg_ingest.py .

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN echo ${PYTHONPATH}
RUN mkdir test_output

CMD [ "python", "test.py" ]