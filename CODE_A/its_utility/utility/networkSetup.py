#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
# https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

import sys
import json
import time
import datetime
import subprocess
import os, traceback

## 환경설정 파일(JSON) 읽기
def readConfig(name):
    with open(name) as json_file:  
        return json.load(json_file)

def system_cmd(cmd): # ex: system_cmd(['ls', '-l'])
    try:
        # result = subprocess.run(cmd, stdout=subprocess.PIPE)
        result = subprocess.check_output(cmd, shell=True)
        return result.decode('utf-8')
    except:
        return None

def wifi_ap_info():
    result = system_cmd('ifconfig wlan0 up') # 디바이스 활성화
    result = system_cmd('iwlist wlan0 scan | grep -E "ESSID" | sed "s/^ *//"') # 디바이스 정보 추출 
    ap_list = result.replace('ESSID:', '').replace('"', '').splitlines() # Ex: ESSID:"ITS-2.4G" -> ITS-2.4G
    return(list(dict.fromkeys(ap_list))) # 중복 제거

def main():
    result = system_cmd('whoami') # SUDO 사용자 여부
    if result is None: 
        exit("error: Sudo User")
    if "root" not in result:
        exit("sudo를 사용하시오")

    print(wifi_ap_info()) # Wifi AP SSID 출력

    ###########################
    ## SD Card Mount
    ###########################
    result = system_cmd('mount -l | grep /mnt') # Check Unmount /mnt
    if result:
        system_cmd('umount /mnt') # SD Card /mnt에 마운트
        system_cmd('umount /media/pi/rootfs') # SD Card /mnt에 마운트

    result = system_cmd('mount /dev/sda2 /mnt') # SD Card /mnt에 마운트
    if result is None: 
        exit("error: Mount Disk")

    dt = datetime.datetime.today().strftime('%Y-%m-%d_%H:%M:%S') # 실행일시

    result = system_cmd('lsblk -nbo size /dev/sda2') # SD Card 삽입 여부
    if result is None: 
        exit("error: SD Device Check")
    if not result.rstrip("\n").isnumeric():
        exit("SD Card 정보가 없습니다.")

    ###########################
    ## device 선택
    ###########################
    while True:
        isWifi = input("Wifi Setup? [y/n]: ") or "n"
        if isWifi is "n":
            ap_device = "eth0"
            break
        elif isWifi is "y":
            ap_device = "wlan0"
            break
        else:
            print("Must type y or n")


    ###########################
    ## wpa_supplicant
    ###########################
    if ap_device == "wlan0":
        ap_name = input("Enter the AP Name : ") or cfg["wpa"]["name"] # AP Name
        while True:
            ap_keys = input("Enter the AP Key : ") or cfg["wpa"]["keys"] # AP Key
            if len(ap_keys) < 8:
                print("Must be 8..63 characters")
            else:
                break
        result = system_cmd("wpa_passphrase {} {}".format(ap_name, ap_keys)) # Key 암호화
        if result is None: 
            exit("error: wpa_passphrase")

        ap_info = "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\ncountry=US\n"
        wpa_conf = ap_info + result # wpa_supplicant 파일 정의

        # wpa_supplicant 사본생성 및 wpa_supplicant 파일 생성 
        print("\n>>>>>>>>>>>\n{0}<<<<<<<<<<<\n".format(wpa_conf))
        ap_confirm = input("Confirm [y] to Save and Update: ") or "n"
        if ap_confirm == "y":
            os.rename(cfg["wpa"]["path"], cfg["wpa"]["path"]+"."+dt) # 원본 복사
            print("Backup to {}\n".format(cfg["wpa"]["path"]+"."+dt))
            f = open(cfg["wpa"]["path"],mode='w')
            f.write(wpa_conf)
            f.close()

    ###########################
    ## interfaces
    ###########################
    ap_addr = input("Enter address : ") or cfg["iface"]["address"] # AP Name
    ap_netm = input("Enter netmask : ") or cfg["iface"]["netmask"] # AP Name
    ap_gate = input("Enter gateway : ") or cfg["iface"]["gateway"] # AP Name
    ap_netw = input("Enter network : ") or cfg["iface"]["network"] # AP Name
    ap_broad = input("Enter broadcast : ") or cfg["iface"]["broadcast"] # AP Name

    if ap_device == "eth0":
        ap_allow = "auto eth0\niface eth0 inet static"
    else:
        ap_allow = "allow-hotplug wlan0\niface wlan0 inet static\nwpa-conf /etc/wpa_supplicant/wpa_supplicant.conf"

    ap_iface = """# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d
auto lo
iface lo inet loopback

{5}
address {0}
netmask {1}
gateway {2}
network {3}
broadcast {4}

# allow-hotplug eth1
# iface eth1 inet static
# address 192.168.168.10
# netmask 255.255.255.0

# allow-hotplug eth2
# iface eth2 inet static
# address 192.168.167.10
# netmask 255.255.255.0

# allow-hotplug eth3
# iface eth3 inet static
# address 192.168.166.10
# netmask 255.255.255.0
""".format(ap_addr, ap_netm, ap_gate, ap_netw, ap_broad, ap_allow)

    # interfaces 사본생성 및 interfaces 파일 생성 
    print("\n>>>>>>>>>>>\n{0}<<<<<<<<<<<\n".format(ap_iface))
    ap_confirm = input("Confirm [y] to Save and Update: ") or "N"
    if ap_confirm == "y":
        os.rename(cfg["iface"]["path"], cfg["iface"]["path"]+"."+dt) # 원본 복사
        print("Backup to {0}\n".format(cfg["iface"]["path"]+"."+dt))
        f = open(cfg["iface"]["path"],mode='w')
        f.write(ap_iface)
        f.close()

    ###########################
    ## SD Card un Mount
    ###########################
    system_cmd('umount /mnt') # SD Card /mnt에 마운트
    system_cmd('umount /media/pi/rootfs') # SD Card /mnt에 마운트
    time.sleep(2)
    print('Now you can remove SD Card.')

if __name__ == "__main__":
    # 파이선 버전 확인
    if sys.version_info.major == 2:
        print('Ex: $ sudo python3 networkSetup.py')
        exit(0)

    configJson = "/home/pi/utility/networkSetup.json"
    if os.path.isfile(configJson):
        cfg = readConfig(configJson)
    else: # 환경설정이 없으면 기본
        cfg = {
            "iface": {
                "address":"192.168.0.130",
                "netmask":"255.255.255.0",
                "gateway":"192.168.0.1",
                "network":"192.168.0.0",
                "broadcast":"192.168.0.255",
                "path":"/mnt/etc/network/interfaces"
            },
            "wpa": {
                "name":"ITS_AP",
                "keys":"GXnLRNT9H50yKQ3G",
                "path":"/mnt/etc/wpa_supplicant/wpa_supplicant.conf"
            }
        }
        
    try:
        main()
    except KeyboardInterrupt:
        result = system_cmd('umount /mnt') # SD Card /mnt에 마운트
        print ("\nCancelled")
    except Exception as e:
        result = system_cmd('umount /mnt') # SD Card /mnt에 마운트
        print(str(e))
        traceback.print_exc()
        os._exit(1)