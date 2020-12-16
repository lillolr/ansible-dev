Role Name
=========

Dell PowerMax Flash Storage Arrays require additional software available from https://github.com/dell/ansible-powermax to run. Despite the documentation provided by https://github.com/dell/ansible-powermax the easiest way to access the required Dell EMC PowerMax modules is by using their (not well advertised) role (which makes accessible an Ansible collection). I was the first download on the Dell EMC PowerMax role / collection, so I know it is not being widely used. However, it's very easy to use with the following instructions

- Install the role / collection with the instructions on https://galaxy.ansible.com/dellemc/powermax
- Now reference this collection at the top of your playbook, this reference allows ansible to use the Dell EMC PowerMax modules. If you never used a collection, check out some of the example playbooks packaged with this role. It's pretty easy.

After following the above steps, this role may be used to expand volume(s) by providing a list of dictionaries, documenting the wwn to expand, and the size (in GB) to expand that wwn to.

If a WWN cannot be expanded, it is written into the file, "failed-wwns-(ansible_date_time.epoch).yml"

Dell EMC reached out to me to provide automation solutions for their Dell EMC PowerMax product. I'm an automation consultant / trainer, so, if you need help Automating your Dell EMC infrastructure, we should talk! I'd love to run a training solution for you and your team! See my author info at the bottom of the module for ways to reach out to me.

Requirements
------------

- Install the role / collection with the instructions on https://galaxy.ansible.com/dellemc/powermax
- Reference the `dellemc.powermax` collection at the top of each playbook
- (Alternatively) Follow the instructions found within the documentation on https://github.com/dell/ansible-powermax to 'hard install' the prerequisite dependencies to avoid referencing the `dellemc.powermax` collection in every playbook solution

Role Variables
--------------

        ## The following variables are HARDCODED into the role
        usv: "90" ## Per docs, this appears to be always set to 90 (for now)
        vc: False ## verify cert set to false for testing purposes
        un: smc  ## This is the USER NAME for the DELL PMAX
        pw: smc  ## This is the PASSWORD for the DELL PMAX

        ## The following variable needs to be defined
        # ush: ## define in playbook - IP of unisphere host

        ## this is the format to resize one or more volumes by WWN
        ## This list of dictionaires 'listofwwn2expand' should be defined in an external file
        ## and pointed to when the role is run (see below for example of pointing to file 'wwns_to_expand.yml')
        #listofwwn2expand:
        #  - wwn: 60000970000197900507533030304538 ## a single wwn to expand (int or string is fine)
        #    nsov: 33 ## new size in GB to expand the volume to (int) (total size)
        #  - wwn: 60000970000197900507533030383621 ## a single wwn to expand (int or string is fine)
        #    nsov: 34 ## new size in GB to expand the volume to (int) (total size)

Dependencies
------------

See "Requirements".

Example Playbook
----------------

An example of using this role is below. Notice that the collection is referenced, or the Dell EMC PowerMax modules and plugin must be installed, before Ansible can utilize this role. 

        ---
        - name: Expanding Dell EMC PowerMax volumes by WWN by RZFeeser
          hosts: localhost
          
          vars_files:
            - wwns_to_expand.yml    # define var 'listofwwn2expand'
          
          vars:
            ush: 10.126.70.19   ## IP of unisphere host

          
          collection:
            - dellemc.powermax
            
          roles:
            - dell_powermax_expand_vol_by_wwn

License
-------

BSD

Author Information
------------------

Dell EMC reached out to me to provide automation solutions for their Dell EMC PowerMax product. I'm an automation consultant / trainer, so, if you need help Automating your Dell EMC infrastructure, we should talk! I'd love to run a training solution for you and your team!

Written by Russell Zachary Feeser for Dell EMC. Contact z at rzfeeser.com or just visit rzfeeser.com if you're looking for Ansible training, or using Ansible with Dell EMC products.

Author: Russell Zachary Feeser

Contact:
    email: rzfeeser at gmail.com or z at rzfeeser.com

Profession: Trainer and Consultant

Available for:
    - Ansible
    - Ansible Module Design with Python
    - Ansible for *your vendor(s) here* (no upcharge for custom training!)
    - Network Automation with Python and Ansible
    - Python for API and API Design
    - Python Basics
    - OpenStack
    - 5G
    - 4G LTE
    - IP Multimedia Subsystem
    - Session Initiation Protocol
    - Playing Minecraft and StarCraft II :p
