FROM node:latest

RUN apt-get update && apt-get install python-requests -y

COPY ./reload_books.sh /etc/cron.daily/
COPY ./updateList.py /root/
COPY ./website /root/

WORKDIR /root/website

RUN cd /root/ && npm install && npm install -g csvtojson
RUN chmod +x /etc/cron.daily/reload_books.sh && /etc/cron.daily/reload_books.sh first

CMD [ "npm", "start" ]
