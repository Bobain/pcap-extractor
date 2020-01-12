# pcap-extractors : Extracting data from pcap files

docker stop pcap_extractor
docker rm pcap_extractor
docker build -t pcap_extractor .
sh run.sh <my_directory with .pcap files to convert>