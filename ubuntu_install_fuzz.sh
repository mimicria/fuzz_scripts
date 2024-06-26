#!/usr/bin/env bash


if [ "$EUID" -ne 0 ]
   then echo "Run this script as root"
   exit
fi

echo "- Installing AFLplusplus"
apt-get update
apt-get install -y build-essential python3-dev python3-pip curl automake cmake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools libgtk-3-dev lcov
apt-get install -y lld llvm llvm-dev clang
apt-get install -y gcc-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-dev
git clone https://github.com/AFLplusplus/AFLplusplus
cd AFLplusplus/src
wget -q https://raw.githubusercontent.com/mimicria/fuzz_scripts/main/afl_patch_scr.py
python3 afl_patch_scr.py
cd ..
make source-only NO_NYX=1
make install

echo "- Installing AFL-utils"
cd ~
git clone https://github.com/mimicria/afl-utils.git
cd afl-utils && python3 -m pip install twitter && python3 setup.py install
cd ~
rm -rf afl-utils

echo "- Installing AFL-cov"
cd ~
git clone https://github.com/mimicria/afl-cov.git
mv afl-cov /opt/afl-cov
# chmod ?
ln -s /opt/afl-cov/afl-cov /bin/afl-cov

echo "- Installing Casr"
PATH=$PATH:/root/.cargo/bin
cd ~
curl https://sh.rustup.rs | sh -s -- -y --default-toolchain=nightly --profile=minimal
cargo install casr

wget -q https://raw.githubusercontent.com/mimicria/fuzz_scripts/main/casr-collect.py -P /bin
chmod +x /bin/casr-collect.py && python3 -m pip install termcolor
