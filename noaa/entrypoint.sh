#!/bin/bash

crontab /app/crontab.txt

cron

tail -f /var/log/cron.log
