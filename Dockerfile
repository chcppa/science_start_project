FROM python:3.10 AS base

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY src/ src/
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "src/app.py"]
