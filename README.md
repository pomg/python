# Python development
Setting up the virtual environment for testing and development under Ubuntu

    pip install virtualenvwrapper

    sudo apt install python-virtualenv 
  
    mkdir -p <target folder>
  
    virtualenv <target folder>
  
Activate the virtual environment:

    source <target folder>/bin/activate
  
Deactivate the virtual environment (the 'deactivate' command is available during runtime):

    deactivate
  
# crack_ssh.py

    python3.5 crack_ssh.py -H <target host> -u <user> -F <password list>
