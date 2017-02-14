# khainguyen
# Dockerfile
#
FROM python:3.5
MAINTAINER khainguyen "khainguyenptiter@gmail.com"

RUN apt-get -y update

RUN apt-get install -y python3-pip

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
