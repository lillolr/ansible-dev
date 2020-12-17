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
module: dellemc_powermax_maskingview

version_added: '2.7'

short_description:  Managing masking views on PowerMax/VMAX Storage
                    System

description:
- Managing masking views on PowerMax Storage System includes,
  create masking view with port group, storage group and host or host group,
  rename masking view and delete masking view
- For creating a masking view -
- (i) portgroup_name,
- (ii) sg_name and
- (iii) any one of host_name or hostgroup_name is required.
- All three entities must be present on the array.
- For renaming a masking view, the 'new_mv_name' is required.
  Once a masking view is created, only its name can be changed.
  No underlying entity (portgroup, storagegroup, host or hostgroup)
  can be changed on the MV.

extends_documentation_fragment:
  - dellemc.powermax.dellemc.dellemc_powermax

author:
- Vasudevu Lakhinana (@unknown) <Vasudevu.Lakhinana@dell.com>
- Prashant Rakheja (@prashant-dell) <prashant.rakheja@dell.com>

options:
  mv_name:
    description:
    - The name of the masking view. No Special Character support except
      for _. Case sensitive for REST Calls.
    required: true
    type: str
  portgroup_name:
    description:
    - The name of the existing port group.
    type: str
  host_name:
    description:
    - The name of the existing host.
    -  This parameter is to create an exclusive or host export.
    type: str
  hostgroup_name:
    description:
    - The name of the existing host group.
    - This parameter is used to create cluster export.
    type: str
  sg_name:
    description:
    - The name of the existing storage group.
    type: str
  new_mv_name:
    description:
    - The new name for renaming function. No Special Character support
      except for _. Case sensitive for REST Calls.
    type: str
  state:
    description:
    - Defines whether the masking view should exist or not.
    choices: [ absent, present ]
    required: true
    type: str
  '''

EXAMPLES = r'''
  - name: Create MV with hostgroup
    dellemc_powermax_maskingview:
      unispherehost: '{{unispherehost}}'
      universion: '{{universion}}'
      verifycert: '{{verifycert}}'
      user: '{{user}}'
      password: '{{password}}'
      serial_no: '{{serial_no}}'
      mv_name: '{{mv_name}}'
      portgroup_name: 'Ansible_Testing_portgroup'
      hostgroup_name: 'Ansible_Testing_hostgroup'
      sg_name: 'Ansible_Testing_SG'
      state: 'present'

  - name: Create MV with host
    dellemc_powermax_maskingview:
      unispherehost: '{{unispherehost}}'
      universion: '{{universion}}'
      verifycert: '{{verifycert}}'
      user: '{{user}}'
      password: '{{password}}'
      serial_no: '{{serial_no}}'
      mv_name: '{{mv_name}}'
      portgroup_name: 'Ansible_Testing_portgroup'
      host_name: 'Ansible_Testing_host'
      sg_name: 'Ansible_Testing_SG'
      state: 'present'

  - name: Rename host masking view
    dellemc_powermax_maskingview:
      unispherehost: '{{unispherehost}}'
      universion: '{{universion}}'
      verifycert: '{{verifycert}}'
      user: '{{user}}'
      password: '{{password}}'
      serial_no: '{{serial_no}}'
      mv_name: '{{mv_name}}'
      new_mv_name: 'Ansible_Testing_mv_renamed'
      state: 'present'

  - name: Delete host masking view
    dellemc_powermax_maskingview:
      unispherehost: '{{unispherehost}}'
      universion: '{{universion}}'
      verifycert: '{{verifycert}}'
      user: '{{user}}'
      password: '{{password}}'
      serial_no: '{{serial_no}}'
      mv_name: 'Ansible_Testing_mv_renamed'
      state: 'absent'
'''

RETURN = r''' '''

import logging
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.powermax.plugins.module_utils \
    import dellemc_ansible_utils as utils

LOG = utils.get_logger('dellemc_powermax_maskingview',
                       log_devel=logging.INFO)
HAS_PYU4V = utils.has_pyu4v_sdk()
PYU4V_VERSION_CHECK = utils.pyu4v_version_check()


class PowerMaxMaskingView(object):
    """Class with masking view operations"""

    def __init__(self):
        """Define all the parameters required by this module"""

        self.module_params = \
            utils.get_powermax_management_host_parameters()
        self.module_params.update(
            get_powermax_masking_view_parameters())

        mutually_exclusive = [
            ['host_name', 'hostgroup_name']
        ]

        # initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            mutually_exclusive=mutually_exclusive
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
        self.provisioning = self.u4v_conn.provisioning
        LOG.info('Got PyU4V instance for provisioning on PowerMax')

    def get_masking_view(self, mv_name):
        """Get details of a given masking view"""

        try:
            mv_list = self.provisioning.get_masking_view_list()
            if mv_name not in mv_list:
                LOG.info('Masking view %s is not present in system', mv_name)
                return None
            LOG.info('Getting masking view %s details', mv_name)
            return self.provisioning.get_masking_view(mv_name)
        except Exception as e:
            LOG.error('Got error %s while getting details of masking '
                      'view %s', str(e), mv_name)
            return None

    def is_mv_changed(self, mv):

        is_mv_changed = False
        if 'portGroupId' in mv \
            and self.module.params['portgroup_name'] is not None \
            and mv['portGroupId'] \
                != self.module.params['portgroup_name']:
            is_mv_changed = True

        elif 'storageGroupId' in mv \
            and self.module.params['sg_name'] is not None \
                and mv['storageGroupId'] != self.module.params['sg_name']:
            is_mv_changed = True

        elif 'hostId' in mv \
            and self.module.params['host_name'] is not None \
                and mv['hostId'] != self.module.params['host_name']:
            is_mv_changed = True

        elif 'hostGroupId' in mv \
            and self.module.params['hostgroup_name'] is not None \
            and mv['hostGroupId'] \
                != self.module.params['hostgroup_name']:
            is_mv_changed = True

        elif 'hostId' in mv and \
                self.module.params['hostgroup_name'] is not None:
            is_mv_changed = True

        elif 'hostGroupId' in mv \
                and self.module.params['host_name'] is not None:
            is_mv_changed = True

        if is_mv_changed:
            error_message = 'One or more of parameters (PG, SG, ' \
                            'Host/Host Group) provided for the MV ' \
                            '{0} differ from the state of the MV on ' \
                            'the array.'.format(mv['maskingViewId'])
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)

    def create_masking_view(self, mv_name):
        """Create masking view with given SG, PG and Host(s)"""

        pg_name = self.module.params['portgroup_name']
        sg_name = self.module.params['sg_name']
        host_name = self.module.params['host_name']
        hostgroup_name = self.module.params['hostgroup_name']

        if host_name and hostgroup_name:
            error_message = 'Failed to create masking view {0},' \
                            'Please provide either host or ' \
                            'hostgroup'.format(mv_name)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
            return False
        elif (pg_name is None) or (sg_name is None) or \
                (host_name is None and hostgroup_name is None):
            error_message = 'Failed to create masking view {0},' \
                            ' Please provide SG, PG and host / host ' \
                            'group name' \
                            ' to create masking view'.format(mv_name)
            LOG.error(error_message)
            self.module.fail_json(msg=error_message)
            return False
        try:
            LOG.info('Creating masking view %s ', mv_name)
            resp = self.provisioning\
                .create_masking_view_existing_components(
                    port_group_name=pg_name, masking_view_name=mv_name,
                    storage_group_name=sg_name, host_name=host_name,
                    host_group_name=hostgroup_name)
            return True, resp
        except Exception as e:
            LOG.error('Failed to create masking view %s with error %s',
                      mv_name, str(e))
            self.module.fail_json(msg='Create masking view {0} failed; '
                                      'error {1}'.format(mv_name,
                                                         str(e)))

    def delete_masking_view(self, mv_name):
        """Delete masking view from system"""

        try:
            self.provisioning.delete_masking_view(mv_name)
            return True
        except Exception as e:
            LOG.error('Delete masking view %s failed with error %s ',
                      mv_name, str(e))
            self.module.fail_json(msg='Delete masking view {0} failed '
                                      'with error {1}.'
                                  .format(mv_name, str(e)))

    def rename_masking_view(self, mv_name, new_mv_name):
        """Rename existing masking view with given name"""

        changed = False
        if mv_name == new_mv_name:
            return changed
        try:
            self.provisioning.rename_masking_view(mv_name, new_mv_name)
            changed = True
        except Exception as e:
            LOG.error('Rename masking view %s failed with error %s ',
                      mv_name, str(e))
            self.module.fail_json(msg='Rename masking view {0} failed '
                                      'with error {1}.'.format(mv_name,
                                                               str(e)))
        return changed

    def perform_module_operation(self):
        """Perform different actions on masking view based on user
        parameter chosen in playbook
        """

        state = self.module.params['state']
        mv_name = self.module.params['mv_name']
        new_mv_name = self.module.params['new_mv_name']

        masking_view = self.get_masking_view(mv_name)
        if masking_view is not None:
            self.is_mv_changed(masking_view)

        result = dict(
            changed=False,
            create_mv='',
            modify_mv='',
            delete_mv='',
        )

        if state == 'present' and not masking_view \
           and not new_mv_name and mv_name:
            LOG.info('Creating masking view %s ', mv_name)
            result['create_mv'], result['mv_details'] = \
                self.create_masking_view(mv_name)

        if state == 'present' and masking_view and new_mv_name:
            LOG.info('Renaming masking view %s ', mv_name)
            result['modify_mv'] = self.rename_masking_view(mv_name,
                                                           new_mv_name)
            mv_name = new_mv_name

        if state == 'absent' and masking_view:
            LOG.info('Delete masking view %s ', mv_name)
            result['delete_mv'] = self.delete_masking_view(mv_name)

        if state == 'present' and masking_view:
            updated_mv = self.get_masking_view(mv_name)
            result['mv_details'] = updated_mv

        if result['create_mv'] or result['modify_mv'] \
           or result['delete_mv']:
            result['changed'] = True

        # Finally update the module changed state!!!
        self.module.exit_json(**result)


def get_powermax_masking_view_parameters():
    """This method provides the parameters required for ansible
    masking view module"""

    return dict(
        mv_name=dict(required=True, type='str'),
        portgroup_name=dict(required=False, type='str'),
        host_name=dict(required=False, type='str'),
        hostgroup_name=dict(required=False, type='str'),
        sg_name=dict(required=False, type='str'),
        new_mv_name=dict(required=False, type='str'),
        state=dict(required=True, choices=['present', 'absent'],
                   type='str')
    )


def main():
    """Create PowerMax masking view object and perform action on it
    based on user input from playbook"""

    obj = PowerMaxMaskingView()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
