# Ansible Modules for Dell EMC Isilon
The Ansible Modules for Dell EMC Isilon allow Data Center and IT administrators to use RedHat Ansible to automate and orchestrate the configuartion and management of Dell EMC Isilon arrays.

The capabilities of the Ansible modules are managing users, groups, access zones, file system, nfs exports, smb shares, snapshots, snapshot schedules and smart quotas; and to gather facts from the array. The tasks can be executed by running simple playbooks written in yaml syntax.

## Supported Platforms
  * Dell EMC Isilon Arrays version 8.0 and above.

## Prerequisites
  * Ansible 2.9 or higher
  * Python 3.5 or higher
  * Red Hat Enterprise Linux 7.6
  * Python SDK for Isilon ( version 8.1.1 )

## Idempotency
The modules are written in such a way that all requests are idempotent and hence fault-tolerant. It essentially means that the result of a successfully performed request is independent of the number of times it is executed.

## List of Ansible Modules for Dell EMC Isilon
  * File System Module
  * Access Zone Module
  * Users Module
  * Groups Module
  * Snapshot Module
  * Snapshot Schedule Module
  * NFS Module
  * SMB Module
  * Smart Quota Module
  * Gather Facts Module

## Installation of SDK
Install python [sdk](https://pypi.org/project/isi-sdk-8-1-1/) named 'isi-sdk-8-1-1'. It can be installed using pip, based on appropriate python version.

## Installing Collections

  * Download the tar build and follow the below command to install the collection anywhere in your system:
		ansible-galaxy collection install dellemc-isilon-1.1.1.tar.gz -p ./collections

  * Set the environemnt variable:
		export ANSIBLE_COLLECTIONS_PATHS=$ANSIBLE_COLLECTIONS_PATHS:<install_path>/collections

## Using Collections

  *	In order to use any  Ansible module, ensure that the importing of proper FQCN(Fully Qualified Collection Name) must be embedded in the playbook. Below example can be referred.
		collections:
		- dellemc.isilon

  * For generating Ansible documentaion for a specific module, embed the FQCN  before the module name. Below example can be referred.
		ansible-doc dellemc.isilon.dellemc_isilon_gatherfacts

## Running Ansible Modules

The Ansible server must be configured with Python library for OneFS to run the Ansible playbooks. The [Documents]( https://github.com/dell/ansible-isilon/tree/1.1.0/dellemc_ansible/docs ) provide information on different Ansible modules along with their functions and syntax. The parameters table in the Product Guide provides information on various parameters which needs to be configured before running the modules.

## SSL Certificate Validation

 * Export the SSL certificate using KeyStore Explorer tool or from the browser in .crt format.
 * Append the SSL certificate to the Certifi package file cacert.pem.
    * For Python 3.5 : cat <<path of the certificate>>  >> /usr/local/lib/python3.5/dist-packages/certifi/cacert.pem
    * For Python 2.7 : cat <<path of the certificate>>  >> /usr/local/lib/python2.7/dist-packages/certifi/cacert.pem
## Results
Each module returns the updated state and details of the entity. 
For example, if you are using the group module, all calls will return the updated details of the group.
Sample result is shown in each module's documentation.

## Support
  * Ansible modules for Isilon are supported by Dell EMC and are provided under the terms of the license attached to the source code.
  * For any setup, configuration issues, questions or feedback, join the [Dell EMC Automation community](https://www.dell.com/community/Automation/bd-p/Automation).
  * For any Dell EMC storage issues, please contact Dell support at: https://www.dell.com/support.
  * Dell EMC does not provide support for any source code modifications.