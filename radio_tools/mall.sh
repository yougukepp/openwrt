#!/bin/bash
#make clean

cp ./radio_tools/5350.config ./.config

make menuconfig
make -j8 #V=99

#cp ./bin/ramips/openwrt-ramips-rt305x-mpr-a2-squashfs-sysupgrade.bin /var/www/ftp/rt5350
#chmod 777 /var/www/ftp/rt5350

#rm -rf ./bin/*

