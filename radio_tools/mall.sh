#!/bin/bash
#make clean

cp ./radio_tools/5350.config ./.config

make menuconfig
make -j8 #V=99

cp ./bin/ramips/openwrt-ramips-rt305x-mpr-a2-squashfs-sysupgrade.bin /tftp/rt5350
chmod 777 /tftp/rt5350

rm -rf ./bin/*

