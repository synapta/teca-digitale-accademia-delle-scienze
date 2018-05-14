FROM node:latest

COPY ./website /root/

WORKDIR /root/website

CMD [ "npm", "start" ]
