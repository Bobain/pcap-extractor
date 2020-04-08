#!/usr/bin/env bash

# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS-2017/pcaps/" "/Volumes/ELEMENTS/downlods/CICIDS-2017/nfdump/" "pcap2netflow.py" "/Volumes/ELEMENTS/tmp/"

# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS2018/Original_Network_Traffic_and_Log_data/" "/Volumes/ELEMENTS/downlods/CICIDS2018/nfdump_netflow" "/Volumes/ELEMENTS/tmp/"
# capWIN-J6GMIG1DQE5-172.31.67.62

# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS2018/Original_Network_Traffic_and_Log_data/" "/Volumes/ELEMENTS/downlods/CICIDS2018/zeek_out" "/Volumes/ELEMENTS/tmp/"



# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS-2017/pcaps" "/Volumes/ELEMENTS/downlods/CICIDS-2017/pcaps/pcap_zeek" "pcap2zeek_logs.py"

# sh run.sh "/Volumes/ELEMENTS/downlods/CICIDS-2017/pcaps" "/Volumes/ELEMENTS/downlods/CICIDS-2017/pcaps/pcap_zeek"

ARG3=${3:-pcap2netflow.py}
ARG4=${4:-/tmp}
ARG5=${5:-pcap_extractor}


docker stop $ARG5
docker rm $ARG5
docker build -f ./src/docker/Dockerfile -t $ARG5 .
# docker run --name=$ARG5 -it $ARG4 /bin/bash


# docker run --name=$ARG5 -it --cpuset-cpus="0-1" -v "$1":/data_in -v "$2":/data_out -v "$ARG4":/tmp $ARG5 /bin/bash

# docker run --name=$ARG5 -it --cpuset-cpus="0-1" -v "$1":/data_in -v "$2":/data_out -v "$ARG4":/tmp $ARG5 /bin/bash

# -c "python3 $ARG3"

docker run --name=$ARG5 --cpuset-cpus="0-1" -v "$1":/data_in -v "$2":/data_out -v "$ARG4":/tmp $ARG5 /bin/bash -c "python3 $ARG3"

# docker run --name=$ARG5 -v "$1":/data_in -v "$2":/data_out -v "$ARG4":/tmp $ARG5

# sh run.sh "/Users/romainburgot/Monday-WorkingHours.pcap" "/Volumes/Elements/data_out" test_pcap
# sh run.sh "/Volumes/SSD EVO/Original Network Traffic and Log data/" "/Users/romainburgot/data_out/"



