FROM ubuntu:latest

LABEL name="textractor"
LABEL version="1.1" maintainer="Evan Oliver <olleit@gmail.com>"
LABEL description="Text Extractor Service"
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE

RUN apt-get update && \
apt-get install -y locales apt-utils python3 python3-pip libev-dev \
&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
&& apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG en_US.utf8

WORKDIR /usr/src/app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8060
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
CMD [ "python3", "./app.py" ]
