FROM python:3.10-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy python scripts
COPY send2dropbox.py .
COPY fetch_data.py .
COPY logger.py .
COPY url_mapping.py .

# Copy entrypoint and crontab files
COPY .env .

RUN chmod +x send2dropbox.py fetch_data.py logger.py url_mapping.py

CMD ["python", "fetch_data.py"]