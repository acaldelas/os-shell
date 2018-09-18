#! /usr/bin/env python3
######################
#Alan Caldelas
#9-16-18
#Shell lab
######################

import os, sys, time, re

pid = os.getpid()

os.write(1, ("about to fork (pid: %d)\n" %pid).encode())
prompt = '$'
def cmd(user_input):
    rc = os.fork()

    if(rc < 0):
        os.write(2, ("Fork failed, returning %\n" %rc).encode())
        sys.exit(1)
    elif(rc == 0):
        cmd = user_input.split()
        args = ["python"]
        for words in cmd:
            args.append

    
command = input(prompt)
