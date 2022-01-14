# paychex coding challen
A python script that automates copying files from remote Server A and transfers them to remote Server B
Information used to login to the servers is pulled from a config.env file which should be created locally.
For demo purposes, I set up to Ubuntu virtual machines locally using VM ware and installed ssh tools on both.

## Requirements for this lab
# - Python3
# - VM WARE Software
# - UBUNTU ISO


## SET UP Virtual Machines
# Install ssh tools on virtual machines using apt command in terminal ```sudo apt install openssh-server```
# Open ssh on virtual machines  ```sudo ufw allow ssh```

## MODULE REQUIREMENTS FOR PYTHON SCRIPT
# need to install dotenv and pathlib to read from env file
# need to install paramiko using pip3 (used to SSH into servers)
# need to install scp module - used for securely copying files between servers. install using  pip3 install (used to copy files) https://pypi.org/project/scp/
BELOW ARE IMPORT STATEMENTS OF REQUIRED MODULES. ALL NON NATIVE MODULES CAN BE INSTALLED USING PIP3 
```
import re
import os
import subprocess
import paramiko
from dotenv import load_dotenv
from pathlib import Path
from scp import SCPClient
import glob 
```

This script requires a config.env in the same directory level as the copy.py file
It should have the following values

config.env 
```
USERNAME=usernameforservers
PASSWORD=password_for_servers
SERVER_1=ipaddress_of_source
SERVER_2=ipaddress_of_destination
SSH_PORT=port_for_ssh
```
