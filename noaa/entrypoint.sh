#!/bin/bash

crontab /app/cron.txt

cron

tail -f /var/log/cron.log
