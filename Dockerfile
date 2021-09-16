FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3-pip curl
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade wheel

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /scripts/fos_api_prom_exporter
ADD fos_api_prom_exporter/ /scripts/fos_api_prom_exporter/
ADD requirements.txt /scripts/requirements.txt
RUN pip3 install -r /scripts/requirements.txt
ADD .env /scripts/
ADD app.py /scripts/
ADD *.sh /scripts/
RUN chmod +x /scripts/*.sh

ENTRYPOINT ["/scripts/docker_entrypoint.sh"]