#!/bin/bash
#make clean

cp -rf ./radio_tools/radio_tools/ package/base-files/files/
cp -rf ./radio_tools/config/rc.local.client package/base-files/files/etc/rc.local
cp -rf ./radio_tools/config/config.client ./.config
sync

#make menuconfig
make -j4 #V=99

cp ./bin/ramips/openwrt-ramips-rt305x-mpr-a2-squashfs-sysupgrade.bin /tftp/rt5350.client
cp /tftp/rt5350.client /tftp/1
chmod 777 /tftp/rt5350.client /tftp/1

rm -rf ./bin/*
sync

