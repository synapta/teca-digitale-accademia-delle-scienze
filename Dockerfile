FROM node:latest

RUN apt-get update && apt-get install python-requests -y

COPY ./reload_books.sh /etc/cron.daily/
COPY ./updateList.py /root/
COPY ./website /root/

WORKDIR /root/website

CMD [ "npm", "start" ]
