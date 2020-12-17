# Ansible Modules for Dell EMC PowerMax

The Ansible Modules for Dell EMC PowerMax allow Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuration and management of Dell EMC PowerMax arrays.

The capabilities of Ansible modules are managing volumes, storage groups, ports, port groups, hosts, host groups, masking views, snapshots, and gather high-level facts about the arrays. The options available for each capability are list, show, create, delete, and modify. These tasks can be executed by running simple playbooks written in yaml syntax. The modules are written so that all the operations are idempotent, so making multiple identical requests has the same effect as making a single request.

## Supported Platforms
  * Dell EMC PowerMax Arrays with Unisphere version 9.0

## Prerequisites
  * Ansible 2.9 or higher
  * Python 3.5 or higher
  * Red Hat Enterprise Linux 7.5
  * Python Library for PowerMax (PyU4V) 3.1.3 or higher
  * Please follow Py4UV installation instructions on https://pyu4v.readthedocs.io/

## Idempotency
The modules are written in such a way that all requests are idempotent and hence fault-tolerant. It essentially means that the result of a successfully performed request is independent of the number of times it is executed.

## List of Ansible Modules for Dell EMC PowerMax
  * Volume module
  * Host module
  * Host group module
  * Snapshot module
  * Maskingview module
  * Port module
  * Port group module
  * Storage group module  
  * Gather facts module

## Installing Collections

  * Download the tar build and follow the below command to install the collection anywhere in your system:
		ansible-galaxy collection install dellemc-powermax-1.0.3.tar.gz -p ./collections

  * Set the environemnt variable:
		export ANSIBLE_COLLECTIONS_PATHS=$ANSIBLE_COLLECTIONS_PATHS:<install_path>/collections

## Using Collections

  *	In order to use any  Ansible module, ensure that the importing of proper FQCN(Fully Qualified Collection Name) must be embedded in the playbook. Below example can be refered.
		collections:
		- dellemc.powermax

  * For generating Ansible documentaion for a specific module, embed the FQCN  before the module name. Below example can be refered.
		ansible-doc dellemc.powermax.dellemc_powermax_gatherfacts

## Running Ansible Modules

The Ansible server must be configured with Python library for Unisphere to run the Ansible playbooks. The [Documents]( https://github.com/dell/ansible-powermax/tree/1.0.0/dellemc_ansible/docs ) provide information on different Ansible modules along with their functions and syntax. The parameters table in the Product Guide provides information on various parameters which needs to be configured before running the modules.

## Results
Each module returns the updated state and details of the entity, for example, if you are using the Volume module, all calls will return the updated details of the volume. Sample result is shown in each module's documentation.

## Support
Ansible for PowerMax Modules are supported by Dell EMC and are provided under the terms of the license attached to the source code.
For any setup, configuration issues, questions or feedback, join the [Dell EMC Automation community]( https://www.dell.com/community/Automation/bd-p/Automation ).
For any Dell EMC storage issues, please contact Dell support at: https://www.dell.com/support.
For clarity, Dell EMC does not provide support for any source code modifications.

