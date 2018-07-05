#FROM ubuntu:16.04
#
#MAINTAINER Harjan Knapper

#RUN apt-get update
#RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#RUN echo "deb http://repo.mongodb.org/apt/ubuntu $(cat /etc/lsb-release | grep DISTRIB_CODENAME | cut -d= -f2)/mongodb-org/3.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list
#RUN apt-get update && apt-get install -y mongodb-org
## Create the MongoDB data directory
#RUN mkdir -p /data/db
#
## Expose port #27017 from the container to the host
#EXPOSE 27017
#
## Set default container command
#ENTRYPOINT usr/bin/mongod


FROM mongo:3.2.10

#create DB directory
RUN mkdir -p /data/db

EXPOSE 27017

CMD ["mongod"]