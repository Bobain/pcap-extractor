docker stop cicflow
docker rm cicflow

docker build -t cicflow -f ./src/docker/cicflowmeter3 .

# docker run --name=cicflow -it -v "tmp":/data_in -v "/tmp":/data_out cicflow /bin/bash


docker run --name=cicflow -it -v "/Volumes/ELEMENTS/downlods/CICIDS2018/Original Network Traffic and Log data/Friday-02-03-2018/pcap":/data_in -v "/Users/romainburgot/data_out":/data_out cicflow /bin/bash

# /Volumes/ELEMENTS/downlods/UGR16/march/week3

# /usr/bin/java -classpath $APP_HOME/build/libs/CICFlowMeter-4.0.jar:$APP_HOME/jnetpcap/linux/jnetpcap-1.4.r1425/jnetpcap.jar:$APP_HOME/extra/libs/log4j-core-2.11.0.jar:$APP_HOME/extra/libs/slf4j-log4j12-1.7.25.jar:$APP_HOME/extra/libs/jnetpcap-1.4.r1425-1g.jar:$APP_HOME/extra/libs/junit-4.12.jar:$APP_HOME/extra/libs/commons-lang3-3.6.jar:$APP_HOME/extra/libs/commons-math3-3.5.jar:$APP_HOME/extra/libs/commons-io-2.5.jar:$APP_HOME/extra/libs/weka-stable-3.6.14.jar:$APP_HOME/extra/libs/jfreechart-1.5.0.jar:$APP_HOME/extra/libs/guava-23.6-jre.jar:$APP_HOME/lib/tika-core-1.17.jar:$APP_HOME/extra/libs/log4j-api-2.11.0.jar:$APP_HOME/extra/libs/slf4j-api-1.7.25.jar:$APP_HOME/extra/libs/log4j-1.2.17.jar:$APP_HOME/extra/libs/hamcrest-core-1.3.jar:$APP_HOME/extra/libs/java-cup-0.11a.jar:$APP_HOME/lib/jsr305-1.3.9.jar:$APP_HOME/extra/libs/checker-compat-qual-2.0.0.jar:$APP_HOME/extra/libs/error_prone_annotations-2.1.3.jar:$APP_HOME/extra/libs/j2objc-annotations-1.1.jar:$APP_HOME/extra/libs/animal-sniffer-annotations-1.14.jar cic.cs.unb.ca.ifm.CICFlowMeter /data_in /data_out