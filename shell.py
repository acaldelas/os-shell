
#! usr/bin/env python3

import os, sys, time, re

# Function to run any python command with args
def run_command(command) :
    rc = os.fork()

    if(rc < 0) : # Failed to fork
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif(rc == 0) : # Child
        split_cmd = command.split() # split command into list
        args = ["python"]
        for words in split_cmd :
            args.append(words) # command line arguments
        for dir in re.split(":", os.environ['PATH']) : #try each directory in the path
            program = "%s/%s" % (dir,args[0])
            try :
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError as e :
                print("command not found in: %s" % dir)
                pass # fail quietly

        print("command not found")
        #os.write(2,("Could not execute %s\n" % command).encode())
        sys.exit(1)

    else : # Parent
        childPidCode = os.wait() # Allow child to finish process


# Prints out 
def print_ls() :
    dirFiles = os.listdir()
    for x in dirFiles :
        print(x)


# Changes directory
# still a work in progress
def change_dir(command) :
    cmd_split = command.split()
    cd_split = []
    curr_dir = os.getcwd()
    if(len(cmd_split) > 1) :
        cd_split = re.split("/",cmd_split[1])
        path = ""
        for x in range(len(curr_dir)-len(cd_split)) :
            path += "/"
            path += curr_dir[x]
        print(path)


# Receive input from user to run command
# Typing 'exit' shall end the prompt

while(True) :
    command = input("$ ")
    cmd_array = command.split()
    cmd_type = cmd_array[0] # gets type of command without breaking command arg
    if(cmd_type == "exit") :
        break # break out of loop and end shell session
    elif(cmd_type == "path") : # debug purposes
        print(os.environ['PATH'])
    elif(cmd_type == "") :
        continue # no input go to next iteration
    elif(cmd_type == "ls") :
        print_ls()
    elif(cmd_type == "cd") :
        change_dir(command)
    elif(cmd_type != "") : # python file run with args
        run_command(command)
