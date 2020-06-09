#!/usr/bin/env bash

# exemples:
# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS-2017/pcaps/" "/Volumes/ELEMENTS/downlods/CICIDS-2017/nfdump/" "pcap2netflow.py" "/Volumes/ELEMENTS/tmp/"
# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS2018/Original_Network_Traffic_and_Log_data/" "/Volumes/ELEMENTS/downlods/CICIDS2018/nfdump_netflow" "pcap2netflow.py" "/Volumes/ELEMENTS/tmp/"
#
# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS2018/Original_Network_Traffic_and_Log_data/" "/Volumes/ELEMENTS/downlods/CICIDS2018/zeek_out" "/Volumes/ELEMENTS/tmp/"
# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS2018/Original_Network_Traffic_and_Log_data/" "/Volumes/ELEMENTS/downlods/CICIDS2018/zeek_out" "/Volumes/ELEMENTS/tmp/"
#
# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS-2017/zeek_logs" "/Volumes/ELEMENTS/downlods/CICIDS-2017/zeek_parquet" "zeek_logs2parquet.py"
#
# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS-2017/pcaps/" "/Volumes/ELEMENTS/downlods/CICIDS-2017/ndpi/" "pcap2ndpi.py"

ARG3=${3:-pcap2netflow.py}
ARG4=${4:-/tmp}
ARG5=${5:-pcap_extractor}

docker stop $ARG5
docker rm $ARG5
docker build -f ./src/docker/Dockerfile -t $ARG5 .

# docker run --name=$ARG5 -it --cpuset-cpus="0-1" -v "$1":/data_in -v "$2":/data_out -v "$ARG4":/tmp $ARG5 /bin/bash
# -c "python3 $ARG3"

docker run --name=$ARG5 --cpuset-cpus="0-1" -v "$1":/data_in -v "$2":/data_out -v "$ARG4":/tmp $ARG5 /bin/bash -c "python3 $ARG3"