#!/usr/bin/python
from pandocfilters import toJSONFilter,Para,stringify
from subprocess import Popen, PIPE
import socket

TCP_IP='127.0.0.1'
TCP_PORT=6969
BUFFER_SIZE=1024

plusparas=[]
negparas=[]

log=open("log","a")

def caps(key, value, format, meta):
  if key == 'Para':
    string=stringify(Para(value))
    print >>log,string
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(string)
    data = s.recv(BUFFER_SIZE)
    if data[0] is '+':
      plusparas+=[string]
    elif data[0] is '-':
      plusparas+=[string]
    return  Para(value)

if __name__ == "__main__":
  try:
    toJSONFilter(caps)
  except socket.error:
    pass
  log.close()
