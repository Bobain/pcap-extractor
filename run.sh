#!/usr/bin/env bash

# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS2018/Original\ Network\ Traffic\ and\ Log\ data/Friday-02-03-2018/pcap/" "/Users/romainburgot/tmp"
# capWIN-J6GMIG1DQE5-172.31.67.62

ARG3=${3:-pcap_extractor}

docker stop $ARG3
docker rm $ARG3
docker build -f ./src/docker/Dockerfile -t $ARG3 .
docker run --name=$ARG3 -it $ARG3 /bin/bash


docker run --name=$ARG3 --cpuset-cpus="0-1" -v "$1":/data_in -v "$2":/data_out $ARG3


# docker run --name=$ARG3 -v "$1":/data_in -v "$2":/data_out $ARG3

# sh run.sh "/Users/romainburgot/Monday-WorkingHours.pcap" "/Volumes/Elements/data_out" test_pcap
# sh run.sh "/Volumes/SSD EVO/Original Network Traffic and Log data/" "/Users/romainburgot/data_out/"

