#!/bin/bash

# 1. 현재 사용되고 있는 이더넷 포트를 확인한다.(eth0 기준으로 설명)
# # ifconfig
# : 현재 세팅되어 있는 네트워크 정보들을 확인할 수 있다.
# : 본인의 IP 를 192.168.0.99 라고 가정한다.
 
 
# 2. IP 를 추가 등록 해보자.
# # ifconfig eth0:1 192.168.1.10 netmask 255.255.255.0 broadcast 192.168.1.255
# : 192.168.0.100 IP 를 추가로 올리는 작업이다.
# # ifconfig eth0:1 192.168.1.10 up
# : 간략하게 위와 같이 해도 IP 를 추가할 수 있다.
 
 
# 3. 사용 후 가상 IP를 삭제하는 방법
# # ifconfig eth0:1 down
# : 0:1 의 가상 IP를 삭제하는 방법이다.
# : 여러 개를 추가했다면 ifconfig 로 정확한 IP 확인 후 삭제하도록 하자.

# # sudo ifconfig eth0:0 192.168.1.10 up
# # sudo ifconfig eth0:0 down
kill $(ps aux | grep 'optex_BSS01.pyc' | awk '{print $2}')