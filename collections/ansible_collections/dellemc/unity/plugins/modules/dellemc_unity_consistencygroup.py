#!/usr/bin/python
# Copyright: (c) 2020, DellEMC

"""Ansible module for managing consistency group on Unity"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r"""
module: dellemc_unity_consistencygroup
version_added: '1.1.0'
short_description: Manage consistency groups on Unity storage system
description:
- Managing the consistency group on the Unity storage system includes
  creating new consistency group, adding volumes to consistency
  group, removing volumes from consistency group, renaming consistency group,
  modifying attributes of consistency group and deleting consistency group.

extends_documentation_fragment:
  - dellemc.unity.dellemc_unity.unity

author:
- Akash Shendge (@shenda1) <ansible.team@dell.com>

options:
  cg_name:
    description:
    - The name of the consistency group.
    - It is mandatory for create operation.
    - Specify either cg_name or cg_id (but not both) for any operation.
    required: False
    type: str
  cg_id:
    description:
    - The ID of the consistency group.
    - It can be used only for get, modify, add/remove volumes or delete
      operations.
    required: False
    type: str
  volumes:
    description:
    - This is a list of volumes.
    - Either the volume ID or name must be provided for adding/removing
      existing volumes from consistency group.
    - If volumes are given, then vol_state should also be specified.
    - Volumes cannot be added/removed from consistency group, if the
      consistency group or the volume has snapshots.
    type: list
    elements: dict
  vol_state:
    description:
    - String variable, describes the state of volumes inside consistency
      group.
    - If volumes are given, then vol_state should also be specified.
    choices: [present-in-group , absent-in-group]
    type: str
  new_cg_name:
    description:
     - The new name of the consistency group, used in rename operation.
    type: str
  description:
    description:
    - Description of the consistency group.
    type: str
  snap_schedule:
    description:
    - Snapshot schedule assigned to the consistency group.
    - Specifying an empty string "" removes the existing snapshot schedule
      from Consistency Group.
    type: str
  tiering_policy:
    description:
    - Tiering policy choices for how the storage resource data will be
      distributed among the tiers available in the pool.
    choices: ['AUTOTIER_HIGH', 'AUTOTIER', 'HIGHEST', 'LOWEST']
    type: str
  state:
    description:
    - Define whether the consistency group should exist or not.
    choices: [absent, present]
    required: true
    type: str
"""

EXAMPLES = r"""
- name: Create consistency group
  dellemc_unity_consistencygroup:
      unispherehost: "{{unispherehost}}"
      verifycert: "{{verifycert}}"
      username: "{{username}}"
      password: "{{password}}"
      cg_name: "{{cg_name}}"
      description: "{{description}}"
      snap_schedule: "{{snap_schedule1}}"
      state: "present"

- name: Get details of consistency group using id
  dellemc_unity_consistencygroup:
      unispherehost: "{{unispherehost}}"
      username: "{{username}}"
      password: "{{password}}"
      verifycert: "{{verifycert}}"
      cg_id: "{{cg_id}}"
      state: "present"

- name: Add volumes to consistency group
  dellemc_unity_consistencygroup:
      unispherehost: "{{unispherehost}}"
      username: "{{username}}"
      password: "{{password}}"
      verifycert: "{{verifycert}}"
      cg_id: "{{cg_id}}"
      volumes:
          - vol_name: "Ansible_Test-3"
          - vol_id: "sv_1744"
      vol_state: "{{vol_state_present}}"
      state: "present"

- name: Rename consistency group
  dellemc_unity_consistencygroup:
      unispherehost: "{{unispherehost}}"
      username: "{{username}}"
      password: "{{password}}"
      verifycert: "{{verifycert}}"
      cg_name: "{{cg_name}}"
      new_cg_name: "{{new_cg_name}}"
      state: "present"

- name: Modify consistency group details
  dellemc_unity_consistencygroup:
      unispherehost: "{{unispherehost}}"
      username: "{{username}}"
      password: "{{password}}"
      verifycert: "{{verifycert}}"
      cg_name: "{{new_cg_name}}"
      snap_schedule: "{{snap_schedule2}}"
      tiering_policy: "{{tiering_policy1}}"
      state: "present"

- name: Remove volumes from consistency group
  dellemc_unity_consistencygroup:
      unispherehost: "{{unispherehost}}"
      username: "{{username}}"
      password: "{{password}}"
      verifycert: "{{verifycert}}"
      cg_name: "{{new_cg_name}}"
      volumes:
        - vol_name: "Ansible_Test-3"
        - vol_id: "sv_1744"
      vol_state: "{{vol_state_absent}}"
      state: "present"

- name: Delete consistency group
  dellemc_unity_consistencygroup:
      unispherehost: "{{unispherehost}}"
      username: "{{username}}"
      password: "{{password}}"
      verifycert: "{{verifycert}}"
      cg_name: "{{new_cg_name}}"
      state: "absent"
"""

RETURN = r'''
changed:
    description: Whether or not the resource has changed
    returned: always
    type: bool

consistency_group_details:
    description: Details of the consistency group
    returned: When consistency group exists
    type: complex
    contains:
        id:
            description:
                - The system ID given to the consistency group
            type: str
        relocation_policy:
            description:
                - FAST VP tiering policy for the consistency group
            type: str
        snap_schedule:
            description: Snapshot schedule applied to consistency group
            type: complex
            contains:
                UnitySnapSchedule:
                    description: Snapshot schedule applied to consistency
                     group
                    type: complex
                    contains:
                        id:
                            description:
                                - The system ID given to the snapshot schedule
                            type: str
                        name:
                            description:
                                - The name of the snapshot schedule
                            type: str
        luns:
            description: Details of volumes part of consistency group
            type: complex
            contains:
                UnityLunList:
                    description: List of volumes part of consistency group
                    type: complex
                    contains:
                        UnityLun:
                            description: Detail of volume
                            type: complex
                            contains:
                                id:
                                    description:
                                        - The system ID given to volume
                                    type: str
                                name:
                                    description:
                                        - The name of the volume
                                    type: str
        snapshots:
            description: List of snapshots of consistency group
            type: complex
            contains:
                name:
                    description:
                        - Name of the snapshot
                    type: str
                creation_time:
                    description:
                        - Date and time on which the snapshot was taken
                    type: str
                expirationTime:
                    description:
                        - Date and time after which the snapshot will expire
                    type: str
                storageResource:
                    description: Storage resource for which the snapshot was
                     taken
                    type: complex
                    contains:
                        UnityStorageResource:
                            description: Details of the storage resource
                            type: complex
                            contains:
                                id:
                                    description:
                                        - The id of the storage resource
                                    type: str
'''

import logging
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.unity.plugins.module_utils.storage.dell \
    import dellemc_ansible_unity_utils as utils

LOG = utils.get_logger('dellemc_unity_consistencygroup',
                       log_devel=logging.INFO)

HAS_UNITY_SDK = utils.get_unity_sdk()

UNITY_SDK_VERSION_CHECK = utils.storops_version_check()


class UnityConsistencyGroup(object):

    """Class with consistency group operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_unity_management_host_parameters()
        self.module_params.update(get_unity_consistencygroup_parameters())

        mutually_exclusive = [['cg_name', 'cg_id']]
        required_one_of = [['cg_name', 'cg_id']]
        required_together = [['volumes', 'vol_state']]

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            mutually_exclusive=mutually_exclusive,
            required_one_of=required_one_of,
            required_together=required_together
        )

        if not HAS_UNITY_SDK:
            self.module.fail_json(msg="Ansible modules for Unity require the"
                                      " Unity python library to be "
                                      "installed. Please install the library "
                                      "before using these modules.")

        if UNITY_SDK_VERSION_CHECK and not UNITY_SDK_VERSION_CHECK[
                'supported_version']:
            err_msg = UNITY_SDK_VERSION_CHECK['unsupported_version_message']
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        self.unity_conn = utils.get_unity_unisphere_connection(
            self.module.params)

    def return_cg_instance(self, cg_name):
        """Return the Consistency Group instance.
            :param cg_name: The name of the consistency group
            :return: Instance of the consistency group
        """

        try:
            cg_details = self.unity_conn.get_cg(name=cg_name)
            cg_id = cg_details.get_id()
            cg_obj = utils.cg.UnityConsistencyGroup.get(self.unity_conn._cli,
                                                        cg_id)
            return cg_obj

        except Exception as e:
            msg = "Failed to get the consistency group {0} instance with " \
                  "error {1}".format(cg_name, str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def get_details(self, cg_id=None, cg_name=None):
        """Get consistency group details.
            :param cg_id: The id of the consistency group
            :param cg_name: The name of the consistency group
            :return: Dict containing consistency group details if exists
        """

        id_or_name = cg_id if cg_id else cg_name
        errormsg = "Failed to get details of consistency group {0} with" \
                   " error {1}"

        try:
            cg_details = self.unity_conn.get_cg(_id=cg_id, name=cg_name)
            if cg_name is None:
                cg_name = cg_details.name

            if cg_details.existed:
                cg_obj = self.return_cg_instance(cg_name)
                snapshots = cg_obj.snapshots

                snapshot_list = [snap._get_properties() for snap in snapshots]

                cg_ret_details = cg_details._get_properties()
                cg_ret_details['snapshots'] = snapshot_list

                # Add volume name to the dict
                if cg_ret_details['luns'] is not None:
                    for i in range(len(cg_details.luns)):
                        cg_ret_details['luns']['UnityLunList'][i]['UnityLun'][
                            'name'] = cg_details.luns[i].name

                # Add snapshot schedule name to the dict
                if cg_ret_details['snap_schedule'] is not None:
                    cg_ret_details['snap_schedule']['UnitySnapSchedule'][
                        'name'] = cg_details.snap_schedule.name

                return cg_ret_details
            else:
                LOG.info("Failed to get details of consistency group %s",
                         id_or_name)
                return None

        except utils.HttpError as e:
            if e.http_status == 401:
                auth_err = "Incorrect username or password, {0}".format(
                    e.message)
                msg = errormsg.format(id_or_name, auth_err)
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            else:
                msg = errormsg.format(id_or_name, str(e))
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        except utils.UnityResourceNotFoundError as e:
            msg = errormsg.format(id_or_name, str(e))
            LOG.error(msg)
            return None

        except Exception as e:
            msg = errormsg.format(id_or_name, str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def get_volume_details(self, vol_name=None, vol_id=None):
        """Get the details of a volume.
            :param vol_name: The name of the volume
            :param vol_id: The id of the volume
            :return: Dict containing volume details if exists
        """

        id_or_name = vol_id if vol_id else vol_name

        try:
            lun = self.unity_conn.get_lun(name=vol_name, _id=vol_id)

            cg = None
            if lun.existed:
                lunid = lun.get_id()
                unitylun = utils.UnityLun.get(self.unity_conn._cli, lunid)
                if unitylun.cg is not None:
                    cg = unitylun.cg
            else:
                errormsg = "The volume {0} not found.".format(id_or_name)
                LOG.error(errormsg)
                self.module.fail_json(msg=errormsg)

            cg_details = self.get_details(
                cg_id=self.module.params['cg_id'],
                cg_name=self.module.params['cg_name'])

            # Check if volume is already part of another consistency group
            if cg is None:
                return lun._get_properties()['id']

            errormsg = "The volume {0} is already part of consistency group" \
                       " {1}".format(id_or_name, cg.name)

            if cg_details is None:
                LOG.error(errormsg)
                self.module.fail_json(msg=errormsg)

            if cg.id != cg_details['id']:
                LOG.error(errormsg)
                self.module.fail_json(msg=errormsg)

            return lun._get_properties()['id']

        except Exception as e:
            msg = "Failed to get the volume {0} with error {1}".format(
                id_or_name, str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def remove_volumes_from_cg(self, cg_name, volumes):
        """Remove volumes from consistency group.
            :param cg_name: The name of the consistency group
            :param volumes: The list of volumes to be removed
            :return: Boolean value to indicate if volumes are removed from
             consistency group
        """

        cg_details = self.unity_conn.get_cg(name=cg_name)._get_properties()
        existing_volumes_in_cg = cg_details['luns']
        existing_vol_ids = []

        if existing_volumes_in_cg:
            existing_vol_ids = [vol['UnityLun']['id'] for vol in
                                existing_volumes_in_cg['UnityLunList']]

        ids_to_remove = []
        vol_name_list = []
        vol_id_list = []

        for vol in volumes:
            if 'vol_id' in vol and not (vol['vol_id'] in vol_id_list):
                vol_id_list.append(vol['vol_id'])
            elif 'vol_name' in vol and not (vol['vol_name'] in vol_name_list):
                vol_name_list.append(vol['vol_name'])

        """remove volume by name"""
        for vol in vol_name_list:
            id = self.get_volume_details(vol_name=vol)
            if id and (id in existing_vol_ids):
                if id not in ids_to_remove:
                    ids_to_remove.append(id)
            else:
                msg = "Unable to remove volume {0} since it is not " \
                      "present in consistency group {1}".format(vol, cg_name)
                LOG.info(msg)

        """remove volume by id"""
        for vol in vol_id_list:
            """verifying if volume id exists in array"""

            if vol in existing_vol_ids and vol not in ids_to_remove:
                ids_to_remove.append(vol)
            else:
                msg = "Unable to remove volume {0} since it is not " \
                      "present in consistency group {1}".format(vol, cg_name)
                LOG.info(msg)

        LOG.info("Volume IDs to remove %s", ids_to_remove)

        if len(ids_to_remove) == 0:
            return False

        vol_remove_list = []
        for vol in ids_to_remove:
            vol_dict = {"id": vol}
            vol_remove_list.append(vol_dict)

        cg_obj = self.return_cg_instance(cg_name)

        try:
            cg_obj.modify(lun_remove=vol_remove_list)
            return True
        except Exception as e:
            errormsg = "Remove existing volumes from consistency group {0} " \
                       "failed with error {1}".format(cg_name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def add_volumes_to_cg(self, cg_name, volumes, tiering_policy):
        """Add volumes to consistency group.
            :param cg_name: The name of the consistency group
            :param volumes: The list of volumes to be added to consistency
             group
            :param tiering_policy: The tiering policy that is to be applied to
            consistency group
            :return: The boolean value to indicate if volumes are added to
             consistency group
        """

        cg_details = self.unity_conn.get_cg(name=cg_name)._get_properties()
        existing_volumes_in_cg = cg_details['luns']
        existing_vol_ids = []

        if existing_volumes_in_cg:
            existing_vol_ids = [vol['UnityLun']['id'] for vol in
                                existing_volumes_in_cg['UnityLunList']]

        ids_to_add = []
        vol_name_list = []
        vol_id_list = []

        for vol in volumes:
            if 'vol_id' in vol and not (vol['vol_id'] in vol_id_list):
                vol_id_list.append(vol['vol_id'])
            elif 'vol_name' in vol and not(vol['vol_name'] in vol_name_list):
                vol_name_list.append(vol['vol_name'])

        """add volume by name"""
        for vol in vol_name_list:
            id = self.get_volume_details(vol_name=vol)
            if id and (id not in existing_vol_ids):
                if id not in ids_to_add:
                    ids_to_add.append(id)
            else:
                msg = "Unable to add volume name {0}, either it doesn't" \
                      " exist or already in volume group ".format(vol)
                LOG.info(msg)

        """add volume by id"""
        for vol in vol_id_list:
            """verifying if volume id exists in array"""
            vol_by_id = self.get_volume_details(vol_id=vol)

            if vol_by_id not in existing_vol_ids:
                if vol_by_id not in ids_to_add:
                    ids_to_add.append(vol_by_id)
            else:
                msg = "Unable to add volume id {0}, either it doesn't" \
                      " exist or already in volume group ".format(vol)
                LOG.info(msg)

        LOG.info("Volume IDs to add %s", ids_to_add)

        if len(ids_to_add) == 0:
            return False

        vol_add_list = []
        for vol in ids_to_add:
            vol_dict = {"id": vol}
            vol_add_list.append(vol_dict)

        cg_obj = self.return_cg_instance(cg_name)

        policy_enum = None
        if tiering_policy:
            if utils.TieringPolicyEnum[tiering_policy]:
                policy_enum = utils.TieringPolicyEnum[tiering_policy]
            else:
                errormsg = "Invalid choice {0} for tiering policy".format(
                    tiering_policy)
                LOG.error(errormsg)
                self.module.fail_json(msg=errormsg)

        try:
            cg_obj.modify(lun_add=vol_add_list, tiering_policy=policy_enum)
            return True
        except Exception as e:
            errormsg = "Add existing volumes to consistency group {0} " \
                       "failed with error {1}".format(cg_name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def rename_cg(self, cg_name, new_cg_name):
        """Rename consistency group.
            :param cg_name: The name of the consistency group
            :param new_cg_name: The new name of the consistency group
            :return: Boolean value to indicate if consistency group renamed
        """
        cg_obj = self.return_cg_instance(cg_name)

        try:
            cg_obj.modify(name=new_cg_name)
            return True
        except Exception as e:
            errormsg = "Rename operation of consistency group {0} failed " \
                       "with error {1}".format(cg_name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def is_cg_modified(self, cg_details):
        """Check if the desired consistency group state is different from
            existing consistency group.
            :param cg_details: The dict containing consistency group details
            :return: Boolean value to indicate if modification is needed
        """
        modified = False

        if self.module.params['tiering_policy'] and cg_details['luns'] is\
                None and self.module.params['volumes'] is None:
            self.module.fail_json(msg="The system cannot assign a tiering"
                                      " policy to an empty Consistency group."
                                  )

        if ((cg_details['description'] is not None and
             self.module.params['description'] is not None and
             cg_details['description'] != self.module.params['description'])
                or (cg_details['description'] is None and
                    self.module.params['description'] is not None)):
            modified = True
        elif ((cg_details['snap_schedule'] is not None and
               self.module.params['snap_schedule'] is not None and
               cg_details['snap_schedule']['UnitySnapSchedule']['name'] !=
               self.module.params['snap_schedule']) or
              (cg_details['snap_schedule'] is None and
               self.module.params['snap_schedule'])):
            modified = True

        if cg_details['relocation_policy']:
            tier_policy = cg_details['relocation_policy'].split('.')
            if self.module.params['tiering_policy'] is not None and\
                    tier_policy[1] != self.module.params['tiering_policy']:
                modified = True

        return modified

    def create_cg(self, cg_name, description, snap_schedule):
        """Create a consistency group.
            :param cg_name: The name of the consistency group
            :param description: The description of the consistency group
            :param snap_schedule: The name of the snapshot schedule
            :return: The boolean value to indicate if consistency group
             created and also returns the CG object
        """

        try:
            if snap_schedule is not None:
                snap_schedule = {"name": snap_schedule}

            cg_obj = utils.cg.UnityConsistencyGroup.create(
                self.unity_conn._cli, name=cg_name, description=description,
                snap_schedule=snap_schedule)
            return True, cg_obj
        except Exception as e:
            errormsg = "Create operation of consistency group {0} failed" \
                       " with error {1}".format(cg_name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def modify_cg(self, cg_name, description, snap_schedule, tiering_policy):
        """Modify Consistency Group.
            :param cg_name: The name of the consistency group
            :param description: The description of the consistency group
            :param snap_schedule: The name of the snapshot schedule
            :param tiering_policy: The tiering policy that is to be applied to
            consistency group
            :return: The boolean value to indicate if consistency group
             modified
        """
        cg_obj = self.return_cg_instance(cg_name)
        is_snap_schedule_paused = None

        if self.module.params['snap_schedule'] == "":
            is_snap_schedule_paused = False

        if snap_schedule is not None:
            if snap_schedule == "":
                snap_schedule = {"name": None}
            else:
                snap_schedule = {"name": snap_schedule}

        policy_enum = None
        if tiering_policy:
            if utils.TieringPolicyEnum[tiering_policy]:
                policy_enum = utils.TieringPolicyEnum[tiering_policy]
            else:
                errormsg = "Invalid choice {0} for tiering policy".format(
                    tiering_policy)
                LOG.error(errormsg)
                self.module.fail_json(msg=errormsg)

        try:
            cg_obj.modify(description=description,
                          snap_schedule=snap_schedule,
                          tiering_policy=policy_enum,
                          is_snap_schedule_paused=is_snap_schedule_paused)
            return True

        except Exception as e:
            errormsg = "Modify operation of consistency group {0} failed " \
                       "with error {1}".format(cg_name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def delete_cg(self, cg_name):
        """Delete consistency group.
        :param cg_name: The name of the consistency group
        :return: The boolean value to indicate if consistency group deleted
        """
        cg_obj = self.return_cg_instance(cg_name)

        try:
            cg_obj.delete()
            return True

        except Exception as e:
            errormsg = "Delete operation of consistency group {0} failed " \
                       "with error {1}".format(cg_name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def validate_volumes(self, volumes):
        """Validate the volumes.
            :param volumes: List of volumes
        """

        for vol in volumes:
            if ('vol_id' in vol) and ('vol_name' in vol):
                errormsg = "Both name and id are found for volume {0}. No" \
                           " action would be taken. Please specify either" \
                           " name or id.".format(vol)
                LOG.error(errormsg)
                self.module.fail_json(msg=errormsg)
            elif 'vol_id' in vol and (len(vol['vol_id'].strip()) == 0):
                errormsg = "vol_id is blank. Please specify valid vol_id."
                LOG.error(errormsg)
                self.module.fail_json(msg=errormsg)
            elif 'vol_name' in vol and (len(vol.get('vol_name').strip()) == 0):
                errormsg = "vol_name is blank. Please specify valid vol_name."
                LOG.error(errormsg)
                self.module.fail_json(msg=errormsg)
            elif 'vol_name' in vol:
                self.get_volume_details(vol_name=vol['vol_name'])
            elif 'vol_id' in vol:
                self.get_volume_details(vol_id=vol['vol_id'])
            else:
                errormsg = "Expected either vol_name or vol_id, found" \
                           " neither for volume {0}".format(vol)
                LOG.error(errormsg)
                self.module.fail_json(msg=errormsg)

    def perform_module_operation(self):
        """
        Perform different actions on consistency group module based on
        parameters chosen in playbook
        """
        cg_name = self.module.params['cg_name']
        cg_id = self.module.params['cg_id']
        description = self.module.params['description']
        volumes = self.module.params['volumes']
        snap_schedule = self.module.params['snap_schedule']
        new_cg_name = self.module.params['new_cg_name']
        tiering_policy = self.module.params['tiering_policy']
        vol_state = self.module.params['vol_state']
        state = self.module.params['state']

        # result is a dictionary that contains changed status and consistency
        # group details
        result = dict(
            changed=False,
            create_cg='',
            modify_cg='',
            rename_cg='',
            add_vols_to_cg='',
            remove_vols_from_cg='',
            delete_cg='',
            consistency_group_details=''
        )

        cg_details = self.get_details(cg_id=cg_id, cg_name=cg_name)

        if cg_name is None and cg_details:
            cg_id = None
            cg_name = cg_details['name']

        if volumes:
            self.validate_volumes(volumes)

        modified = False

        if cg_details:
            modified = self.is_cg_modified(cg_details)

        if vol_state and not volumes:
            self.module.fail_json(msg="Specify volumes along with vol_state")

        if state == 'present' and not cg_details:
            if not volumes and tiering_policy:
                self.module.fail_json(msg="The system cannot assign a"
                                          " tiering policy to an empty"
                                          " Consistency group")

            if not cg_name:
                msg = "The parameter cg_name length is 0. It is too short." \
                      " The min length is 1."
                self.module.fail_json(msg=msg)

            if new_cg_name:
                self.module.fail_json(msg="Invalid argument, new_cg_name is"
                                          " not required")

            result['create_cg'], cg_details = self.create_cg(
                cg_name, description, snap_schedule)
        elif state == 'absent' and cg_details:
            if cg_details['luns']:
                self.module.fail_json(msg="Please remove all volumes which"
                                          " are part of consistency group"
                                          " before deleting it.")
            result['delete_cg'] = self.delete_cg(cg_name)

        if state == 'present' and vol_state == 'present-in-group' and \
                cg_details and volumes:
            result['add_vols_to_cg'] = self.add_volumes_to_cg(cg_name,
                                                              volumes,
                                                              tiering_policy)
        elif state == 'present' and vol_state == 'absent-in-group' and \
                cg_details and volumes:
            result['remove_vols_from_cg'] = self.remove_volumes_from_cg(
                cg_name, volumes)

        if state == 'present' and new_cg_name is not None:
            if not new_cg_name:
                msg = "The parameter new_cg_name length is 0. It is too" \
                      " short. The min length is 1."
                self.module.fail_json(msg=msg)

            if cg_name != new_cg_name:
                result['rename_cg'] = self.rename_cg(cg_name, new_cg_name)
                cg_name = new_cg_name

        if state == 'present' and cg_details and modified:
            result['modify_cg'] = self.modify_cg(cg_name, description,
                                                 snap_schedule, tiering_policy
                                                 )

        if result['create_cg'] or result['modify_cg'] or result[
            'add_vols_to_cg'] or result['remove_vols_from_cg'] or result[
                'delete_cg'] or result['rename_cg']:
            result['changed'] = True

        result['consistency_group_details'] = self.get_details(cg_id=cg_id,
                                                               cg_name=cg_name
                                                               )
        self.module.exit_json(**result)


def get_unity_consistencygroup_parameters():
    """This method provide parameters required for the ansible consistency
        group module on Unity"""
    return dict(
        cg_name=dict(required=False, type='str'),
        cg_id=dict(required=False, type='str'),
        description=dict(required=False, type='str'),
        volumes=dict(required=False, type='list', elements='dict'),
        snap_schedule=dict(required=False, type='str'),
        new_cg_name=dict(required=False, type='str'),
        tiering_policy=dict(required=False, type='str', choices=[
            'AUTOTIER_HIGH', 'AUTOTIER', 'HIGHEST', 'LOWEST']),
        vol_state=dict(required=False, type='str',
                       choices=['present-in-group', 'absent-in-group']),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create Unity consistency group object and perform action on it
        based on user input from playbook"""
    obj = UnityConsistencyGroup()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
