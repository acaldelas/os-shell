#! usr/bin/env python3
######################
#Alan Caldelas
#9-16-19
#Shell lab
######################

import os, sys, time, re

pid = os.getpid()

os.write(1,("about to fork(pid=%d)\n" % pid).encode())
def cmd_redirect(user_input,):
    rc = os.fork()

    if(rc<0):
        os.write(2, ("fork failed returning %d\n" % rc).encode())
        sys.exit(1)
    elif(rc ==0):
        spl = user_input.split()
        args = [spl]

        os.close(1)

        sys.stdout = open("results.txt", "w")
        fd = sys.stdout.fileno()
        os.set_inheritable(fd, True)
        os.write(2, ("Child: opened fd = %d for writing\n" % fd).encode())
        
        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError as e:
                print("Command not found in: %s" % dir)
                pass
        print("Command not found")
        sys.exit(1)

    else:
        childPID = os.wait()
def print_ls():
    dirFiles = os.listdir()
    for x in dirFiles:
        print(x)

def change_dir(command):
    split_cmd = command.split()
    cd_split = []
    current_directory = os.getcwd()
    if(len(split_cmd) > 1):
        cd_split = re.split("/",split_cmd[1])
        path = ""
        for x in range(len(current_directory) - len(cd_split)):
            
            path += current_directory[x]
        print(path)






while(True):
    command = input("$ ")
    cmd_array = command.split()
    cmd_type = cmd_array[0]
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
        cmd(command)