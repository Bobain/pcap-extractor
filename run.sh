# docker run --name=pcap_extractor -d -v $1:/data pcap_extractor

# docker run --name=pcap_extractor -v "/Users/romainburgot/Documents/CIC IDS 2017":/data pcap_extractor


docker stop pcap_extractor
docker rm pcap_extractor
docker build -t pcap_extractor .
docker run --name=pcap_extractor -v "/Users/romainburgot/Documents/CIC IDS 2017":/data pcap_extractor
# /bin/bash