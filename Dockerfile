FROM python:3.8.0-buster

ARG SERVER_NAME

RUN dpkg --add-architecture i386
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install libstdc++6:i386 libgcc1:i386 libcurl4-gnutls-dev:i386 libsdl2-2.0-0:i386

RUN mkdir -p /steamcmd
WORKDIR "/steamcmd"
RUN wget "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
RUN tar -xvzf steamcmd_linux.tar.gz

WORKDIR "/"
COPY scripts /scripts

RUN mkdir -p /.klei/DoNotStarveTogether
COPY build /.klei/DoNotStarveTogether/$SERVER_NAME

RUN chmod -R a+rwx /.klei
# caves stuff
EXPOSE 11001
EXPOSE 27019
EXPOSE 8769

# master stuff
EXPOSE 11000
EXPOSE 27018
EXPOSE 8768

# cluster stuff
EXPOSE 10889

# steam stuff
EXPOSE 27015

ENV server_name=$SERVER_NAME
ENTRYPOINT /scripts/runserver.sh $server_name