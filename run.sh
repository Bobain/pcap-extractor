#!/usr/bin/env bash

# sh run.sh "/Volumes/SSD EVO/Original Network Traffic and Log data/" "/private/nfs/09_JEUX_DE_DONNEES/CU-LID/unb.ca/CIC IDS 2018/"

ARG3=${3:-pcap_extractor}

docker stop $ARG3
docker rm $ARG3
docker build -f ./src/docker/Dockerfile -t $ARG3 .
# docker run --name=$3 -it $ARG3 /bin/bash
docker run --name=$3 --cpuset-cpus="0-2" -v "$1":/data_in -v "$2":/data_out
# -v /Users/romainburgot/tmp:/tmp $ARG3

# docker run --name=$3 -v "$1":/data_in -v "$2":/data_out $ARG3

# sh run.sh "/Users/romainburgot/Monday-WorkingHours.pcap" "/Volumes/Elements/data_out" test_pcap
# sh run.sh "/Volumes/SSD EVO/Original Network Traffic and Log data/" "/Users/romainburgot/data_out/"

