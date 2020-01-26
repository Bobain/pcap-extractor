FROM python:3.7.1

RUN apt-get update
# dependencies for nfdump
RUN apt-get install -y apt-utils vim bison libtool dh-autoreconf libpcap-dev libghc-bzlib-dev flex
# decompressing and other stuff tools
RUN apt-get install -y unzip unrar-free p7zip-full
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wireshark
# zeek additional dependencies
RUN apt-get install -y cmake make gcc g++ bison libssl-dev python-dev swig zlib1g-dev

# < NFDUMP
RUN wget https://github.com/phaag/nfdump/archive/v1.6.18.tar.gz
RUN tar -xf v1.6.18.tar.gz

# compiling it and installing it
RUN cd nfdump-1.6.18 \
    && chmod 777 ./autogen.sh \
    && sh ./autogen.sh \
    && ./configure --enable-sflow --enable-readpcap --enable-nfpcapd \
    && make && make install

# cleaning the mess
RUN rm v1.6.18.tar.gz && rm -rf nfdump-1.6.18

RUN mv /usr/local/lib/libnfdump* /usr/lib/
# >

# < installing Zeek
RUN wget https://github.com/zeek/zeek/releases/download/v3.0.1/zeek-3.0.1.tar.gz
RUN tar zxf zeek-3.0.1.tar.gz

# compiling it and installing it
RUN cd zeek-3.0.1 && ./configure && make && make install

# cleaning the mess
RUN rm zeek-3.0.1.tar.gz && rm -rf zeek-3.0.1

RUN export PATH=/usr/local/zeek/bin:$PATH
# >

# < Python
RUN mkdir /app
WORKDIR /app/
COPY requirements.txt /app/
COPY src/python/ /app/
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -e .
# >

# run nfdump on data
CMD [ "python3", "-u", "pcap2netflow.py" ] #
