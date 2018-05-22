#!/bin/bash

git pull

docker rm teca-accademia
docker rmi teca-accademia

docker build -t teca-accademia .
docker run -d -p 4444:4444 --restart=always --name teca-accademia teca-accademia
