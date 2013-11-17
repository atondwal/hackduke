#!/usr/bin/python
from pandocfilters import toJSONFilter
from subproccess import Popen, PIPE

def caps(key, value, format, meta):
  if key == 'Para':
    p=Popen(['pandoc','-f','json','-t',],stdin=PIPE,stdout=PIPE
    return somefunction(value)

if __name__ == "__main__":
  toJSONFilter(caps)
