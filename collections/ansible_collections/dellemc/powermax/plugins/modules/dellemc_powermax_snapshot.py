#!/usr/bin/python
# Copyright: (c) 2019, DellEMC

from __future__ import absolute_import, division, print_function


__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_powermax_snapshot

version_added: '2.7'

short_description: Manage Snapshots on PowerMax/VMAX Storage System

description:
- Managing Snapshots on PowerMax Storage System includes
  Create a new Storage Group Snapshot,
  Get details of Storage Group Snapshot,
  Rename SG Snapshot,
  Change Snapshot link status,
  Delete an existing Storage Group Snapshot.

author:
- Prashant Rakheja (@prashant-dell) <prashant.rakheja@dell.com>

extends_documentation_fragment:
  - dellemc.powermax.dellemc.dellemc_powermax

options:
  sg_name:
    description:
    - The name of the storage group.
    required: true
    type: str
  snapshot_name:
    description:
    - The name of the Snapshot.
    required: true
    type: str
  ttl:
    description:
    - The Time To Live (TTL) value for the Snapshot.
    - If the ttl is not specified, the storage group snap details would
      be returned.
    - However, to create a SG snap - TTL must be given.
    - If the SG snap should not have any TTL - specify TTL as 'None'
    type: str
  ttl_unit:
    description:
    - The unit for the ttl.
    - If no ttl_unit is specified, 'days' is taken as default ttl_unit.
    choices: [hours, days]
    default: days
    type: str
  generation:
    description:
    - The generation number of the Snapshot.
    - Generation is mandatory for link, unlink, rename and delete
      operations.
    - Optional for Get snapshot details.
    - Create snapshot will always create a new snapshot with generation
      number 0.
    - Rename is supported only for generation number 0.
    type: int
  new_snapshot_name:
    description:
    - The new name of the Snapshot.
    type: str
  target_sg_name:
    description:
    - The target Storage Group.
    type: str
  link_status:
    description:
    - Describes the link status of the Snapshot.
    choices: [linked, unlinked]
    type: str
  state:
    description:
    - Define whether the Snapshot should exist or not.
    required: true
    choices: [absent, present]
    type: str
  '''

EXAMPLES = r'''
  - name: Create a Snapshot for a Storage Group
    dellemc_powermax_snapshot:
      unispherehost: '{{unispherehost}}'
      universion: '{{universion}}'
      verifycert: '{{verifycert}}'
      user: '{{user}}'
      password: '{{password}}'
      serial_no: '{{serial_no}}'
      sg_name: 'ansible_sg'
      snapshot_name: 'ansible_sg_snap'
      ttl: '2'
      ttl_unit: 'days'
      state: 'present'

  - name: Get Storage Group Snapshot details
    dellemc_powermax_snapshot:
      unispherehost: '{{unispherehost}}'
      universion: '{{universion}}'
      verifycert: '{{verifycert}}'
      user: '{{user}}'
      password: '{{password}}'
      serial_no: '{{serial_no}}'
      sg_name: 'ansible_sg'
      snapshot_name: 'ansible_sg_snap'
      state: 'present'

  - name: Delete Storage Group Snapshot
    dellemc_powermax_snapshot:
      unispherehost: '{{unispherehost}}'
      universion: '{{universion}}'
      verifycert: '{{verifycert}}'
      user: '{{user}}'
      password: '{{password}}'
      serial_no: '{{serial_no}}'
      sg_name: 'ansible_sg'
      snapshot_name: 'ansible_sg_snap'
      generation: 1
      state: 'absent'

  - name: Rename Storage Group Snapshot
    dellemc_powermax_snapshot:
      unispherehost: '{{unispherehost}}'
      universion: '{{universion}}'
      verifycert: '{{verifycert}}'
      user: '{{user}}'
      password: '{{password}}'
      serial_no: '{{serial_no}}'
      sg_name: 'ansible_sg'
      snapshot_name: 'ansible_sg_snap'
      new_snapshot_name: 'ansible_snap_new'
      generation: 0
      state: 'present'

  - name: Change Snapshot Link Status to Linked
    dellemc_powermax_snapshot:
      unispherehost: '{{unispherehost}}'
      universion: '{{universion}}'
      verifycert: '{{verifycert}}'
      user: '{{user}}'
      password: '{{password}}'
      serial_no: '{{serial_no}}'
      sg_name: 'ansible_sg'
      snapshot_name: 'ansible_snap_new'
      generation: 1
      target_sg_name: 'ansible_sg_target'
      link_status: 'linked'
      state: 'present'

  - name: Change Snapshot Link Status to UnLinked
    dellemc_powermax_snapshot:
      unispherehost: '{{unispherehost}}'
      universion: '{{universion}}'
      verifycert: '{{verifycert}}'
      user: '{{user}}'
      password: '{{password}}'
      serial_no: '{{serial_no}}'
      sg_name: 'ansible_sg'
      snapshot_name: 'ansible_snap_new'
      generation: 1
      target_sg_name: 'ansible_sg_target'
      link_status: 'unlinked'
      state: 'present'
'''

RETURN = r''' '''

import logging
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powermax.plugins.module_utils \
    import dellemc_ansible_utils as utils

LOG = utils.get_logger('dellemc_powermax_snapshot',
                       log_devel=logging.INFO)
HAS_PYU4V = utils.has_pyu4v_sdk()
PYU4V_VERSION_CHECK = utils.pyu4v_version_check()


class PowerMaxSnapshot(object):
    """Class with Snapshot operations"""

    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = utils\
            .get_powermax_management_host_parameters()
        self.module_params.update(get_powermax_snapshot_parameters())

        # initialize the Ansible module
        self.module = AnsibleModule(argument_spec=self.module_params,
                                    supports_check_mode=False
                                    )

        if HAS_PYU4V is False:
            self.module.fail_json(msg='Ansible modules for PowerMax '
                                      'require the PyU4V python library'
                                      ' to be installed. Please install'
                                      ' the library before using these '
                                      'modules.')

        if PYU4V_VERSION_CHECK is not None:
            self.module.fail_json(msg=PYU4V_VERSION_CHECK)
            LOG.error(PYU4V_VERSION_CHECK)

        self.u4v_conn = utils.get_U4V_connection(self.module.params)
        self.replication = self.u4v_conn.replication
        self.common = self.u4v_conn.common
        LOG.info('Got PyU4V instance for provisioning on PowerMax ')

    def get_snapshot(self, sg_id, snapshot_name, generation):
        """Get snapshot details"""

        try:
            LOG.info('Getting storage group %s snapshot %s details',
                     sg_id, snapshot_name)
            if generation is None:
                return self.replication.\
                    get_storagegroup_snapshot_generation_list(sg_id,
                                                              snapshot_name)
            return self.replication.\
                get_snapshot_generation_details(sg_id,
                                                snapshot_name,
                                                generation)
        except Exception as e:
            error_message = ('Got error: %s while getting details '
                             'of storage group %s snapshot %s',
                             str(e), sg_id, snapshot_name)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_sg_snapshot(self, sg_id, snap_name, ttl, ttl_unit):
        """Create Storage Group Snapshot"""

        try:
            if ttl_unit == 'days':
                ttl_unit = False
            else:
                ttl_unit = True
            if ttl == 'None':
                ttl = None
            resp = self.replication.create_storagegroup_snap(sg_id,
                                                             snap_name,
                                                             ttl,
                                                             ttl_unit)
            return True, resp
        except Exception as e:
            error_message = ('Create Snapshot %s for SG %s '
                             'failed with error %s ', snap_name,
                             sg_id, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def delete_sg_snapshot(self, sg_id, snap_name, generation):
        """Delete Storage Group Snapshot"""

        try:
            snapshot = self.replication\
                .get_snapshot_generation_details(sg_id, snap_name,
                                                 generation)
        except Exception:
            return False
        try:

            if snapshot:
                self.replication\
                    .delete_storagegroup_snapshot(sg_id, snap_name,
                                                  generation)
            return True
        except Exception as e:
            error_message = ('Delete SG %s Snapshot %s failed '
                             'with error %s ', sg_id, snap_name, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def rename_sg_snapshot(self, sg_id, snap_name, new_snap_name,
                           generation):
        """Rename Storage Group Snapshot"""

        try:
            snapshot = self.get_snapshot(sg_id, snap_name, generation)
            if snap_name == new_snap_name:
                return False, snapshot
            resp = self.replication. \
                modify_storagegroup_snap(sg_id,
                                         'None',
                                         snap_name,
                                         generation,
                                         new_name=new_snap_name
                                         )
            return True, resp
        except Exception as e:
            error_message = ('Renaming Snapshot %s for '
                             'Storage Group %s failed with error %s ',
                             snap_name, sg_id, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def change_snapshot_link_status(self, sg_id, target_sg,
                                    snap_name, link_status, generation):
        """Change Snapshot Link status"""

        if generation is None:
            error_message = ('Change SG %s Snapshot %s link status failed. '
                             'Please provide a valid generation ', sg_id,
                             snap_name)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
        try:
            snapshot = self.get_snapshot(sg_id, snap_name, generation)

            if snapshot['isLinked'] is True and link_status == 'linked':
                for linked_sg in snapshot['linkedStorageGroup']:
                    linked = False
                    if linked_sg['name'] == target_sg:
                        linked = True
                        break
                if linked:
                    return False, snapshot
            elif snapshot['isLinked'] is False and link_status == 'unlinked':
                return False, snapshot
            if link_status == 'linked':
                link = True
                unlink = False
            else:
                link = False
                unlink = True
            resp = self.replication. \
                modify_storagegroup_snap(sg_id,
                                         target_sg,
                                         snap_name,
                                         link=link,
                                         unlink=unlink,
                                         gen_num=generation)
            return True, resp
        except Exception as e:
            error_message = ('Change SG %s Snapshot %s link status '
                             'failed with error %s ',
                             sg_id, snap_name, str(e))
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def perform_module_operation(self):
        """Perform different actions on Snapshot based on user parameter
        chosen in playbook
        """

        sg_name = self.module.params['sg_name']
        snapshot_name = self.module.params['snapshot_name']
        ttl = self.module.params['ttl']
        ttl_unit = self.module.params['ttl_unit']
        generation = self.module.params['generation']
        new_snapshot_name = self.module.params['new_snapshot_name']
        target_sg_name = self.module.params['target_sg_name']
        link = self.module.params['link_status']
        state = self.module.params['state']

        result = dict(
            changed=False,
            create_sg_snap='',
            delete_sg_snap='',
            rename_sg_snap='',
            change_snap_link_status='',
        )

        if state == 'present' and ttl and not \
                (new_snapshot_name or link):
            LOG.info('Creating snapshot %s for storage group %s ',
                     snapshot_name, sg_name)
            result['create_sg_snap'], result['sg_snap_details'] = \
                self.create_sg_snapshot(sg_name,
                                        snapshot_name,
                                        ttl,
                                        ttl_unit)
        elif state == 'absent' and generation is not None:
            LOG.info('Delete storage group %s snapshot %s generation '
                     '%s ', sg_name, snapshot_name, generation)
            result['delete_sg_snap'] = self.delete_sg_snapshot(sg_name,
                                                               snapshot_name,
                                                               generation)

        if state == 'present' and snapshot_name \
                and link and target_sg_name:
            LOG.info('Change storage group %s snapshot %s link status',
                     sg_name, snapshot_name)
            result['change_snap_link_status'], \
                result['sg_snap_link_details'] \
                = self.change_snapshot_link_status(sg_name,
                                                   target_sg_name,
                                                   snapshot_name,
                                                   link,
                                                   generation)

        if state == 'present' and sg_name and snapshot_name and \
                new_snapshot_name and generation == 0:
            LOG.info('Rename storage group %s snapshot %s ',
                     sg_name, snapshot_name)
            result['rename_sg_snap'], result['sg_snap_rename_details']\
                = self.rename_sg_snapshot(sg_name,
                                          snapshot_name,
                                          new_snapshot_name,
                                          generation)

        if state == 'present' and not ttl and not link and \
                not new_snapshot_name:
            LOG.info('Returning storage group %s snapshot %s details ',
                     sg_name, snapshot_name)
            result['sg_snap_details'] = self.get_snapshot(sg_name,
                                                          snapshot_name,
                                                          generation)

        if result['create_sg_snap'] or result['delete_sg_snap'] \
           or result['rename_sg_snap'] \
           or result['change_snap_link_status']:
            result['changed'] = True

        # Finally update the module result!
        self.module.exit_json(**result)


def get_powermax_snapshot_parameters():
    return dict(
        sg_name=dict(required=True, type='str'),
        snapshot_name=dict(required=True, type='str'),
        ttl=dict(required=False, type='str'),
        ttl_unit=dict(required=False, default='days',
                      choices=['hours', 'days'], type='str'),
        generation=dict(required=False, type='int'),
        new_snapshot_name=dict(required=False, type='str'),
        target_sg_name=dict(required=False, type='str'),
        link_status=dict(required=False, choices=['linked', 'unlinked'],
                         type='str'),
        state=dict(required=True, choices=['present', 'absent'],
                   type='str'),
    )


def main():
    """Create PowerMax Snapshot object and perform action on it
        based on user input from playbook"""
    obj = PowerMaxSnapshot()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
