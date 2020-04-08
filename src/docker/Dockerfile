FROM python:3.7.1

RUN apt-get update
# dependencies for nfdump
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils vim bison libtool dh-autoreconf libpcap-dev libghc-bzlib-dev flex
# decompressing and other stuff tools
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y unzip unrar-free p7zip-full
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wireshark
# zeek additional dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y cmake make gcc g++ bison libssl-dev python-dev swig zlib1g-dev
# WAND tools (libprotoident) additional dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential libncurses-dev curl apt-transport-https ssl-cert \
    ca-certificates gnupg lsb-release
RUN echo "deb https://dl.bintray.com/wand/general $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/wand.list
RUN curl --silent "https://bintray.com/user/downloadSubjectPublicKey?username=wand" | apt-key add -
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

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

# a script for easy install from tar.gz source code
COPY src/sh/github_install.sh ./

# < installing Zeek
RUN sh github_install.sh https://github.com/zeek/zeek/releases/download/v3.0.1/zeek-3.0.1.tar.gz
ENV PATH /usr/local/zeek/bin:$PATH
# >

# installing nDPI
RUN sh github_install.sh https://github.com/ntop/nDPI/archive/3.0.tar.gz "./autogen.sh"

# < installing libprotoident
# libwandio packages
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libwandio1-dev wandio1-tools
RUN sh github_install.sh https://github.com/wanduow/libwandder/archive/1.2.0-1.tar.gz "./bootstrap.sh"
# installing libtrace
RUN sh github_install.sh https://github.com/LibtraceTeam/libtrace/archive/4.0.10-1.tar.gz "./bootstrap.sh"
ENV LD_LIBRARY_PATH /lib:/usr/lib:/usr/local/lib
# installing libflowmanager
RUN sh github_install.sh https://github.com/wanduow/libflowmanager/archive/v3.0.0.tar.gz "./bootstrap.sh"
# installing libprotoident
RUN sh github_install.sh https://github.com/wanduow/libprotoident/archive/2.0.14-1.tar.gz "./bootstrap.sh"
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
# CMD [ "python3", "-u", "pcap2zeek_logs.py" ] # pcap2netflow.py
