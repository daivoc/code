#!/usr/bin/env python

import subprocess
import re
import sys

curDate = subprocess.check_output ('date "+%Y-%m-%d %H:%M:%S"', shell=True)
running = subprocess.check_output ('uptime -p', shell=True)

disk = subprocess.check_output ('df -h --output=size,used,avail,pcent / | tail -1', shell=True)
dT = re.sub(' +',',',disk.strip()).split(',')

memory = subprocess.check_output ('cat /proc/meminfo  | head -n 2', shell=True)
mT = re.sub(' +',',',memory.strip()).split(',')
mt = mT[1][:-3]
ma = mT[3][:-3]
mu = int(mt) - int(ma)

with open('/sys/class/thermal/thermal_zone0/temp') as temp:
	curCtemp = float(temp.read()) / 1000
	curFtemp = ((curCtemp / 5) * 9) + 32
lastUpWeb = subprocess.check_output ('stat /var/www/html/its_web -c %x', shell=True)
lastUpCode = subprocess.check_output ('stat /home/pi -c %x', shell=True)
unixName = subprocess.check_output ('uname -svr', shell=True)

nodeV = "Node "+subprocess.check_output ('node -v', shell=True)
pythonV = "Python "+sys.version.split(' ')[0]
phpV = "PHP "+subprocess.check_output ('php -v | head -1', shell=True).split(' ')[1]
mysqlV = subprocess.check_output ('mysql -V', shell=True).split(',')[0]
apache2V = subprocess.check_output ('apache2 -v | head -1', shell=True).split(' ')[2]
gnuV = subprocess.check_output ('grep G5_GNUBOARD_VER /var/www/html/its_web/config.php | head -1', shell=True).split("'")[3]

print("Current Time: %s"%curDate)
print("<br>")
print("Running %s"%running)
print("<br>")
print("Disk Total:%s Used:%s(%s) Avail:%s"%(dT[0], dT[1], dT[3], dT[2])) # ' +' : 연속적인 스페이스, .split(',')
print("<br>")
print("Memory Total:%sM Used:%sM Avail:%sM"%(mt, mu, ma)) # ' +' : 연속적인 스페이스, .split(',')
print("<br>")
print("CPU Temp: %s'C"%(curCtemp))
print("<br>")
print("Web Update @%s"%lastUpWeb.split(".")[0])
print("<br>")
print("Code Update@ %s"%lastUpCode.split(".")[0])
print("<br>")
print("OS %s Web %s GNU %s"%(unixName, apache2V, gnuV))
print("<br>")
print("%s, %s, %s, DB %s"%(pythonV, phpV, nodeV, mysqlV))
print("<br>")
print("By Utility's System Status")
