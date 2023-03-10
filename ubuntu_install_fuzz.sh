#!/usr/bin/env bash


if [ "$EUID" -ne 0 ]
   then echo "Run this script as root"
   exit
fi

echo "- Installing AFLplusplus"
apt-get update > /dev/null
apt-get install -y build-essential python3-dev python3-pip curl automake cmake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools libgtk-3-dev > /dev/null
apt-get install -y lld llvm llvm-dev clang > /dev/null
apt-get install -y gcc-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-dev > /dev/null
git clone https://github.com/AFLplusplus/AFLplusplus > /dev/null
cd AFLplusplus > /dev/null 
make source-only NO_NYX=1 > /dev/null
make install 

echo "- Installing AFL-utils"
cd ~ > /dev/null
git clone https://github.com/mimicria/afl-utils.git > /dev/null
cd afl-utils && python3 -m pip install twitter && python3 setup.py install
cd ~ > /dev/null
rm -rf afl-utils > /dev/null

echo "- Installing AFL-cov"
cd ~ > /dev/null
git clone https://github.com/mimicria/afl-cov.git > /dev/null
mv afl-cov /opt/afl-cov > /dev/null
# chmod ?
ln -s /opt/afl-cov/afl-cov /bin/afl-cov

echo "- Installing Fuzzman"
cd ~ > /dev/null
git clone https://github.com/mimicria/fuzzaide.git > /dev/null
cd fuzzaide && pip install . 
cd ~ > /dev/null
rm -rf fuzzaide > /dev/null

echo "- Installing Casr"
PATH=$PATH:/root/.cargo/bin
cd ~ > /dev/null
curl https://sh.rustup.rs | sh -s -- -y --default-toolchain=nightly --profile=minimal > /dev/null
cargo install casr
