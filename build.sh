#!/bin/bash

docker stop gitscanner_instance
docker rm gitscanner_instance 
docker rmi gitscanner

docker build -t gitscanner .
docker run --name gitscanner_instance --restart=always -d -t gitscanner


#docker logs -f gitscanner_instance
