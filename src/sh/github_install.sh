#!/usr/bin/env sh

# only tar gz please!!!

set -x
set -e

# downloading
wget -O /tmp/project2install.tar.gz $1

# uncompressing
mkdir /tmp/project2install && tar zxf /tmp/project2install.tar.gz -C /tmp/project2install --strip-components=1


# Second argument used to do bootstrap or autogen, etc
cd /tmp/project2install
if [ $# -ge 2 ]; then
    "$2"
fi

./configure
make
make install

# cleaning the mess
rm /tmp/project2install.tar.gz && rm -rf /tmp/project2install

set +x