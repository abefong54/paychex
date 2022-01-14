#!/usr/bin/env python3
import re
import os
import subprocess
import paramiko
from dotenv import load_dotenv
from pathlib import Path
from scp import SCPClient
import glob


def getCredentials():
    # function used to read in values from config.env
    # returns username, password, two servier IP's and a port number

    dotenv_path = Path('./config.env')
    load_dotenv(dotenv_path=dotenv_path)

    user = os.getenv('USERNAME')
    pw = os.getenv('PASSWORD')
    server_one = os.getenv('SERVER_1')
    server_two = os.getenv('SERVER_2')
    port = os.getenv('SSH_PORT')

    if not user and not pw:
        print("Error retrieving credentials ~ gracefully terminating ")
        exit

    # TEST SERVER STATUS
    response1 = os.system("ping -c 1 " + server_one)
    response2 = os.system("ping -c 1 " + server_two)
    if not response1 == 0:
        print (server_one, 'is not up!')
        exit 
    if not response2 == 0:
        print (server_two, 'is not up!')
        exit 

    return user, pw, server_one, server_two, port



def sshConnectCopy(source_host,port,username,password):
    # function used to ssh into a source server
    # and copy files from ./files directory

    # set up ssh client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(source_host, port, username, password)

    # get files
    command = "ls ./files"
    stdin, stdout, stderr = ssh.exec_command(command)
    files = stdout.readlines()

    # COPY ALL FILES FOUND TO LOCAL MACHINE
    with SCPClient(ssh.get_transport()) as scp:
        for file in files:
            scp.get("~/files/"+file.rstrip("\n"))


def sshConnectTransfer(dest_host,port,username,password):
    # function used to ssh into a destination server 
    # and copy files into ./files directory

    # SSH INTO DESTINATION
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(dest_host, port, username, password)

    # MAKE A DIRECTORY TO COPY FILES INTO IN DESTINATION
    command = "mkdir ./files"
    stdin, stdout, stderr = ssh.exec_command(command)

    # COPY ALL FILES FROM LOCAL TO DESTINATION SERVER
    with SCPClient(ssh.get_transport()) as scp:
        for file in files_to_copy:
            scp.put(file, recursive=True, remote_path='./files')


if __name__ == "__main__":
    # main function and entry point for our program

    # GRAB CREDENTIALS
    user, pw, source_host, destination_host, port = getCredentials()

    # COPY FILES FROM REMOTE SERVER A
    sshConnectCopy(source_host, port, user, pw)

    #  files from local
    files_to_copy = [f for f in glob.glob("move*.txt")]
    print("\n\nFILES TO COPY:", files_to_copy)

    # TRANSFER FILES TO REMOTE SERVER B
    sshConnectTransfer(destination_host, port, user, pw)

    print("DONE")