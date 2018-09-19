#! usr/bin/env python3
######################
#Alan Caldelas
#9-16-19
#Shell lab
######################

import os, sys, time, re

pid = os.getpid()

os.write(1,("about to fork(pid=%d)\n" % pid).encode())
def cmd_redirect(user_input,user_re, user_out):
    rc = os.fork()

    if(rc<0):
        os.write(2, ("fork failed returning %d\n" % rc).encode())
        sys.exit(1)
    elif(rc ==0):
        spl = user_input.split()
        print(spl)
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
def cmd_2(cmd):
    print("Hello we gotta do some redirecting here...")
    rc = os.fork()
    if rc < 0:
        os.write(2,("Fork failed, returning %d\n" %rc).encode())
        sys.exit(1)
    elif rc == 0:
        args = cmd
        os.close(1)
        sys.stdout = open(args[2], "w")
        os.set_inheritable(1, True)
        for dir in re.split(":", os.environ['PATH']):
            program ="%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError:
                pass
        os.write(2, ("Child: Error: could not exec %s\n" % args[0]).encode())
        sys.exit(1)
    
#No redirect just a simple command
def cmd_1(cmd):
    print("HELLO")
    rc = os.fork()
    
    if rc < 0:
        os.write(2,("Fork failed, returning %d\n" %rc).encode())
        sys.exit(1)
    elif rc ==0:
        args = cmd
        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, args[0])
            os.write(1, ("Child: ... Trying to exec %s\n" %program).encode())
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError:
                pass
        os.write(2,("Child: Could not exec %s\n" %args[0]).encode())
        sys.exit(1)

    
while(True):
    try:
        prompt = input("$ ")
    except EOFError:
        print("\n")
        exit()
    cmd_arr = prompt.split()
    print(f"You entered:{cmd_arr}, {len(cmd_arr)}")
    if cmd_arr[0] == "exit":
        exit()
    elif '>' in cmd_arr:
        cmd_2(cmd_arr)
        os.wait()
    else:
        cmd_1(cmd_arr)
        os.wait()
    
    """    
    print("Entering cmd_1")
    if len(cmd_arr) > 2 and (">") in list:
        cmd_2(cmd_arr)
        
    cmd_1(cmd_arr)
    os.wait()
    print("Hi")"""
        


"""
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
"""
