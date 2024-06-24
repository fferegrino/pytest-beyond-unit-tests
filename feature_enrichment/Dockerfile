FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY *.py ./feature_enrichment/

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["python", "feature_enrichment/main.py"]
