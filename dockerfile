FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y cron busybox
RUN apt-get install -y python3 python3-pip

# Install packages using pip
RUN pip3 install aiohttp pika python-dotenv pymongo

# Copy only necessary files
COPY crontab /etc/cron.d/crontab
COPY scraper.py .env db.py /app/

# Set permissions for cron
RUN chmod 0644 /etc/cron.d/crontab && \
    crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
