#!/usr/bin/python
import os
import subprocess
import sys
import psutil
import syslog
import time

def getram():
  ram = psutil.phymem_usage()
  return ram

if __name__ == '__main__':
  syslog.syslog('Starting Zram...')
  p = subprocess.Popen(["modprobe", "zram"])
  ram = getram()
  size = ram.total / 2
  p.wait()
  try: 
    f = open ('/sys/block/zram0/disksize', 'w')
  except:
    syslog.syslog(syslog.LOG_ERR, 'No zram in sys')
    sys.exit()
  f.write(str(size))
  f.flush()
  f.close
  syslog.syslog('Init swap')
  n = 5
  for i in range(n):
    if os.path.exists('/dev/zram0'):
      break
    else:
      time.sleep(1)
  if os.path.exists('/dev/zram0'):
    p = subprocess.Popen(["mkswap", '/dev/zram0'])
    p.wait()
    p = subprocess.Popen(["swapon", '/dev/zram0'])
  else:
    syslog.syslog(syslog.LOG_ERR, 'No device for zram')
    sys.exit()
  p.wait()
  syslog.syslog('Zram started')

  sys.exit()
