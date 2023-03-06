#!/bin/bash

apt-get update
apt-get install -y cron
apt install -y nano
pip install aiohttp pika python-dotenv pymongo

echo '* * * * * cd /app && /usr/local/bin/python3 /app/scraper.py' > /etc/cron.d/scraper-cron
chmod +x /app/scraper.py
chmod 0644 /etc/cron.d/scraper-cron
/usr/bin/crontab /etc/cron.d/scraper-cron
touch /var/log/cron.log
cron -f
