#!/usr/bin/env bash

# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS2018/Original_Network_Traffic_and_Log_data/" "/Volumes/ELEMENTS/downlods/CICIDS2018/nfdump_netflow" "/Volumes/ELEMENTS/tmp/"
# capWIN-J6GMIG1DQE5-172.31.67.62

ARG4=${4:-pcap_extractor}
ARG3=${3:-/tmp}

docker stop $ARG4
docker rm $ARG4
docker build -f ./src/docker/Dockerfile -t $ARG4 .
# docker run --name=$ARG4 -it $ARG3 /bin/bash


# docker run --name=$ARG4 -it --cpuset-cpus="0-1" -v "$1":/data_in -v "$2":/data_out -v "$ARG3":/tmp $ARG4 /bin/bash


docker run --name=$ARG4 -v "$1":/data_in -v "$2":/data_out -v "$ARG3":/tmp $ARG4

# sh run.sh "/Users/romainburgot/Monday-WorkingHours.pcap" "/Volumes/Elements/data_out" test_pcap
# sh run.sh "/Volumes/SSD EVO/Original Network Traffic and Log data/" "/Users/romainburgot/data_out/"

