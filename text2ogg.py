#!/usr/bin/python
import sys
import subprocess

subprocess.call(['./text2ogg.zsh',sys.argv[1]],stdin=sys.stdin)
