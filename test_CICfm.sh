docker stop cicflow
docker rm cicflow

docker build -t cicflow -f ./src/docker/cicflowmeter .

docker run --name=cicflow -it -v "/Volumes/ELEMENTS/downlods/UGR16/march/week3":/data_in -v "/Users/romainburgot/data_out":/data_out cicflow /bin/bash

#/CICFlowMeter/build/scripts/cfm