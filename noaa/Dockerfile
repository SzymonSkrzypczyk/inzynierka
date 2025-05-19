FROM python:3.10-slim

ENV TZ=Europe/Warsaw

RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy python scripts
COPY send2dropbox.py .
COPY fetch_data.py .
COPY logger.py .
COPY url_mapping.py .

# Copy entrypoint and crontab files
COPY entrypoint.sh .
COPY cron.txt .
COPY .env .

RUN chmod +x entrypoint.sh send2dropbox.py fetch_data.py logger.py url_mapping.py

ENTRYPOINT ["./entrypoint.sh"]