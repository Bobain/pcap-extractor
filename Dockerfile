FROM python:3.7.1

RUN apt-get update
RUN apt-get install -y apt-utils vim bison libtool dh-autoreconf libpcap-dev libghc-bzlib-dev flex

# NFDUMP
# Donwloading nfdump source code
RUN wget https://github.com/phaag/nfdump/archive/v1.6.18.tar.gz
RUN tar -xf v1.6.18.tar.gz

# compiling it and installing it
RUN cd nfdump-1.6.18 && chmod 777 ./autogen.sh && sh ./autogen.sh && ./configure && make && make install

# cleaning the mess
RUN rm v1.6.18.tar.gz && rm -rf nfdump-1.6.18

# Python
RUN mkdir /app
WORKDIR /app/
COPY requirements.txt /app/
COPY src/python/ /app/
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -e .

RUN mv /usr/local/lib/libnfdump* /usr/lib/

# mount shared volume

# CMD [ "python3", "-u", "pcap2netflow.py" ]
