FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./retrieval/
RUN pip install --upgrade pip && pip install -r ./retrieval/requirements.txt

COPY . ./retrieval/

RUN chmod +x ./retrieval/*.py

ENV PYTHONPATH=/app

# Run fetch_data.py by default
ENTRYPOINT ["python", "./retrieval/fetch_data.py"]
