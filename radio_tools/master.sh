#!/bin/bash
#make clean

cp -rf ./radio_tools/radio_tools/ package/base-files/files/
cp -rf ./radio_tools/config/rc.local.master package/base-files/files/etc/rc.local
cp -rf ./radio_tools/config/config.master ./.config
sync

#make menuconfig
make -j4 #V=99

cp ./bin/ramips/openwrt-ramips-rt305x-mpr-a2-squashfs-sysupgrade.bin /tftp/rt5350.master
cp /tftp/rt5350.master /tftp/1
chmod 777 /tftp/rt5350.master /tftp/1

rm -rf ./bin/*
sync
