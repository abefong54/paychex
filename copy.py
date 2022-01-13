#!/usr/bin/env python3

import re
import os
import subprocess
import paramiko
from dotenv import load_dotenv
from pathlib import Path


from scp import SCPClient
import glob



# requred for this lab
# - VM WARE
# - UBUNTU ISO

# need to install ssh on virtual machines 'sudo apt install openssh-server'
# need to open ssh on virtual machines  'sudo ufw allow ssh'

# need to install dotenv and pathlib to read from env file
# need to install paramiko using pip3 (used to SSH into servers)
# need to install scp using pip3 (used to copy files) https://pypi.org/project/scp/

def getCredentials():

    dotenv_path = Path('./config.env')
    load_dotenv(dotenv_path=dotenv_path)

    user = os.getenv('USERNAME')
    pw = os.getenv('PASSWORD')
    server_one = os.getenv('SERVER_1')
    server_two = os.getenv('SERVER_2')
    port = os.getenv('SSH_PORT')

    return user, pw, server_one, server_two, port


user, pw, server_one, server_two, port = getCredentials()

if not user and not pw:
    print("Error retrieving credentials ~ gracefully terminating ")
    exit

response1 = os.system("ping -c 1 " + server_one)
response2 = os.system("ping -c 1 " + server_two)

# TEST TO SEE IF REMOTE SERVERS ARE UP
if response1 == 0:
      print (server_one, 'is up!')
if response2 == 0:
      print (server_two, 'is up!')

# CREDENTIALS

print(user)
print(pw)

username = "abefong54"
password = "3vtwyk3m!"
source_host = server_one
dest_host = server_two
port = 22

# CONNECT TO SERVER ONE
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(source_host, port, username, password)

# LIST ALL FILES TO BE COPIED FROM SOURCE
command = "ls ./files"
stdin, stdout, stderr = ssh.exec_command(command)
files = stdout.readlines()

# COPY ALL FILES FOUND TO LOCAL MACHINE
with SCPClient(ssh.get_transport()) as scp:
    for file in files:
        scp.get("~/files/"+file.rstrip("\n"))

files_to_copy = [f for f in glob.glob("move*.txt")]
print(files_to_copy)


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
        scp.put("~/files/"+file)


# TODO
# COPY FILES INTOT ./files IN DESTINATION
# USE user AND pw READ IN EARLIER FROM TXT FILE
# ADD ERROR CHECKING
# CLEAN UP
