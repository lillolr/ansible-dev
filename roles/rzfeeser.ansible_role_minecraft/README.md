Role Name
=========

ansible-role-minecraft:

    - This role deploys a minecraft server on Debian based system (Debian and Ubuntu).
    - If you have run the role previously, it will STOP the server software, backup the world to /tmp/minecraft_backup/ with the current date, then START the software
    - This role runs the minecraft server software in a screen session titled "minecraft"

Requirements
------------

The role will install some additional apps to help support running the mcserver, these include:
    - default-jre (java required for sever to run)
    - git
    - fail2ban
    - screen
    - vim

Role Variables
--------------

The only variables that need defined are found in vars/main.yml, they are as follows:
    - 
      # avail at https://minecraft.net/en-us/download/server/
      mc_version: 'https://launcher.mojang.com/v1/objects/3dc3d84a581f14691199cf6831b71ed1296a9fdf/server.jar'
    -
      # This should reflect the current version of the Minecraft server
      mc_version_str: "1.14.1"

Dependencies
------------

This role has no other role dependencies.

Example Playbook
----------------

If you want to run the playbook against remote host(s), run the playbook below:


    - name: Deploy the minecraft server
      hosts: minecraft
    
      roles:
              - ansible-minecraft

If you want to run the playbook against the local host (where ansible is installed), run the playbook below.


    - name: Deploy the minecraft server
      hosts: localhost
      connection: local
    
      roles:
              - ansible-minecraft

License
-------

MIT

Author Information
------------------

Author: Russell Zachary Feeser

Contact:
    email: rzfeeser@gmail.com

Profession: Trainer and Consultant

Available for:
    - Ansible
    - Ansible Module Design with Python
    - Network Automation with Python and Ansible
    - Python for API and API Design
    - Python Basics
    - OpenStack
    - 5G
    - 4G LTE
    - IP Multimedia Subsystem
    - Session Initiation Protocol
    - Playing Minecraft and StarCraft II :p
