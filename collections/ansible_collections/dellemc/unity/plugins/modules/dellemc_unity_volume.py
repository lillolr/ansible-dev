#!/usr/bin/python
# Copyright: (c) 2020, DellEMC

"""Ansible module for managing volumes on Unity"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r"""

module: dellemc_unity_volume
version_added: '1.1.0'
short_description: Manage volume on Unity storage system
description:
- Managing volume on Unity storage system includes-
  Create new volume,
  Modify volume attributes,
  Map Volume to host,
  Unmap volume to host,
  Display volume details,
  Delete volume

extends_documentation_fragment:
  - dellemc.unity.dellemc_unity.unity

author:
- Arindam Datta (@arindam-emc) <ansible.team@dell.com>

options:
  vol_name:
    description:
    - The name of the volume. Mandatory only for create operation.
    required: False
    type: str
  vol_id:
    description:
    - The id of the volume.
    - It can be used only for get, modify, map/unmap host or delete operation.
    required: False
    type: str
  pool_name:
    description:
    - This is the name of the pool where the volume will be created.
    - Either the pool_name or pool_id must be provided to create a new volume.
    type: str
  pool_id:
    description:
    - This is the id of the pool where the volume will be created.
    - Either the pool_name or pool_id must be provided to create a new volume.
    type: str
  size:
    description:
     - The size of the volume.
    type: int
  cap_unit:
    description:
     - The unit of the volume size. It defaults to 'GB', if not specified.
    choices: ['GB' , 'TB']
    type: str
  description:
    description:
    - Description about the volume.
    - Description can be removed by passing empty string ("").
    type: str
  snap_schedule:
    description:
    - Snapshot schedule assigned to the volume.
    - Add/Remove/Modify the snapshot schedule for the volume.
    type: str
  compression:
    description:
    - Boolean variable , specifies whether or not to enable compression.
      Compression is supported only for thin volumes
    type: bool
  is_thin:
    description:
    - Boolean variable , specifies whether or not it's a thin volume.
    default: True
    type: bool
  sp:
    description:
    - Storage Processor for this volume.
    choices: ['SPA' , 'SPB']
    type: str
  io_limit_policy:
    description:
    - IO limit policy associated with this volume.
      Once it's set cannot be removed through ansible module but it can
      be changed.
    type: str
  host_name:
    description:
    - Name of the host to be mapped/unmapped with this volume.
    - Either host_name,host_id can be specified in one task along with
      mapping_state.
    type: str
  host_id:
    description:
    - ID of the host to be mapped/unmapped with this volume.
    - Either host_name,host_id can be specified in one task along with
      mapping_state.
    type: str
  hlu:
    description:
    - Host Lun Unit to be mapped/unmapped with this volume.
    - It's an optional parameter, hlu can be specified along
      with host_name or host_id and mapping_state.
    - If hlu is not specified, unity will choose it automatically.
      The maximum value supported is 255.
    type: int
  mapping_state:
    description:
    - State of host access for volume.
    choices: ['mapped' , 'unmapped']
    type: str
  new_vol_name:
    description:
    - New name of the volume for rename operation.
    type: str
  tiering_policy:
    description:
    - Tiering policy choices for how the storage resource data will be
      distributed among the tiers available in the pool.
    choices: ['AUTOTIER_HIGH', 'AUTOTIER', 'HIGHEST', 'LOWEST']
    type: str
  state:
    description:
    - State variable to determine whether volume will exist or not.
    choices: ['absent', 'present']
    required: true
    type: str
"""

EXAMPLES = r"""
- name: Create Volume
  dellemc_unity_volume:
    unispherehost: "{{unispherehost}}"
    username: "{{username}}"
    password: "{{password}}"
    verifycert: "{{verifycert}}"
    vol_name: "{{vol_name}}"
    description: "{{description}}"
    pool_name: "{{pool}}"
    size: 2
    cap_unit: "{{cap_GB}}"
    state: "{{state_present}}"

- name: Expand Volume by volume id
  dellemc_unity_volume:
    unispherehost: "{{unispherehost}}"
    username: "{{username}}"
    password: "{{password}}"
    verifycert: "{{verifycert}}"
    vol_id: "{{vol_id}}"
    size: 5
    cap_unit: "{{cap_GB}}"
    state: "{{state_present}}"

- name: Modify Volume, map host by host_name
  dellemc_unity_volume:
    unispherehost: "{{unispherehost}}"
    username: "{{username}}"
    password: "{{password}}"
    verifycert: "{{verifycert}}"
    vol_name: "{{vol_name}}"
    host_name: "{{host_name}}"
    hlu: 5
    mapping_state: "{{state_mapped}}"
    state: "{{state_present}}"

- name: Modify Volume, unmap host mapping by host_name
  dellemc_unity_volume:
    unispherehost: "{{unispherehost}}"
    username: "{{username}}"
    password: "{{password}}"
    verifycert: "{{verifycert}}"
    vol_name: "{{vol_name}}"
    host_name: "{{host_name}}"
    mapping_state: "{{state_unmapped}}"
    state: "{{state_present}}"

- name: Modify Volume attributes
  dellemc_unity_volume:
    unispherehost: "{{unispherehost}}"
    username: "{{username}}"
    password: "{{password}}"
    verifycert: "{{verifycert}}"
    vol_name: "{{vol_name}}"
    new_vol_name: "{{new_vol_name}}"
    tiering_policy: "AUTOTIER"
    compression: True
    state: "{{state_present}}"

- name: Delete Volume by vol name
  dellemc_unity_volume:
    unispherehost: "{{unispherehost}}"
    username: "{{username}}"
    password: "{{password}}"
    verifycert: "{{verifycert}}"
    vol_name: "{{vol_name}}"
    state: "{{state_absent}}"

- name: Delete Volume by vol id
  dellemc_unity_volume:
    unispherehost: "{{unispherehost}}"
    username: "{{username}}"
    password: "{{password}}"
    verifycert: "{{verifycert}}"
    vol_id: "{{vol_id}}"
    state: "{{state_absent}}"
"""

RETURN = r'''

changed:
    description: Whether or not the resource has changed
    returned: always
    type: bool

volume_details:
    description: Details of the volume
    returned: When volume exists
    type: complex
    contains:
        id:
            description:
                - The system generated ID given to the volume
            type: str
        name:
            description:
                - Name of the volume
            type: str
        description:
            description:
                - description about the volume
            type: str
        is_data_reduction_enabled:
            description:
                - Whether or not compression enabled on this volume
            type: bool
        size_total_with_unit:
            description:
                - Size of the volume with actual unit.
            type: str
        snap_schedule:
            description:
                - Snapshot schedule applied to this volume
            type: dict
        tiering_policy:
            description:
                - Tiering policy applied to this volume
            type: str
        current_sp:
            description:
                - Current storage processor for this volume
            type: str
        pool:
            description:
                - The pool in which this volume is allocated.
            type: dict
        host_access:
            description:
                - Host mapped to this volume
            type: list
        io_limit_policy:
            description:
                - IO limit policy associated with this volume
            type: dict
        wwn:
            description:
                - The world wide name of this volume
            type: str
        is_thin_enabled:
            description:
                - Indicates whether thin provisioning is enabled for this
                  volume
            type: bool
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.unity.plugins.module_utils.storage.dell \
    import dellemc_ansible_unity_utils as utils
import logging


LOG = utils.get_logger('dellemc_unity_volume', log_devel=logging.INFO)

HAS_UNITY_SDK = utils.get_unity_sdk()

UNITY_SDK_VERSION_CHECK = utils.storops_version_check()


class UnityVolume(object):

    """Class with volume operations"""

    param_host_id = None
    param_io_limit_pol_id = None
    param_snap_schedule_name = None

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_unity_management_host_parameters()
        self.module_params.update(get_unity_volume_parameters())

        mutually_exclusive = [['vol_name', 'vol_id'],
                              ['pool_name', 'pool_id'],
                              ['host_name', 'host_id']]

        required_one_of = [['vol_name', 'vol_id']]

        # initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            mutually_exclusive=mutually_exclusive,
            required_one_of=required_one_of)

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

    def get_volume(self, vol_name=None, vol_id=None):
        """Get the details of a volume.
            :param vol_name: The name of the volume
            :param vol_id: The id of the volume
            :return: instance of the respective volume if exist.
        """

        id_or_name = vol_id if vol_id else vol_name
        errormsg = "Failed to get the volume {0} with error {1}"

        try:

            obj_vol = self.unity_conn.get_lun(name=vol_name, _id=vol_id)

            if vol_id and obj_vol.existed:
                LOG.info("Successfully got the volume object %s ", obj_vol)
                return obj_vol
            elif vol_name:
                LOG.info("Successfully got the volume object %s ", obj_vol)
                return obj_vol
            else:
                LOG.info("Failed to get the volume %s", id_or_name)
                return None

        except utils.HttpError as e:
            if e.http_status == 401:
                cred_err = "Incorrect username or password , {0}".format(
                    e.message)
                msg = errormsg.format(id_or_name, cred_err)
                self.module.fail_json(msg=msg)
            else:
                msg = errormsg.format(id_or_name, str(e))
                self.module.fail_json(msg=msg)

        except utils.UnityResourceNotFoundError as e:
            errormsg.format(id_or_name, str(e))
            LOG.error(errormsg)
            return None

        except Exception as e:
            msg = errormsg.format(id_or_name, str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def get_host(self, host_name=None, host_id=None):
        """Get the instance of a host.
            :param host_name: The name of the host
            :param host_id: The id of the volume
            :return: instance of the respective host if exist.
        """

        id_or_name = host_id if host_id else host_name
        errormsg = "Failed to get the host {0} with error {1}"

        try:

            obj_host = self.unity_conn.get_host(name=host_name, _id=host_id)

            if host_id and obj_host.existed:
                LOG.info("Successfully got the host object %s ", obj_host)
                return obj_host
            elif host_name:
                LOG.info("Successfully got the host object %s ", obj_host)
                return obj_host
            else:
                msg = "Failed to get the host {0}".format(id_or_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        except Exception as e:

            msg = errormsg.format(id_or_name, str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def get_snap_schedule(self, name):
        """Get the instance of a snapshot schedule.
            :param name: The name of the snapshot schedule
            :return: instance of the respective snapshot schedule if exist.
        """

        errormsg = "Failed to get the snapshot schedule {0} with error {1}"

        try:
            LOG.debug("Attempting to get Snapshot Schedule with name %s",
                      name)
            obj_ss = utils.UnitySnapScheduleList.get(self.unity_conn._cli,
                                                     name=name)
            if obj_ss and (len(obj_ss) > 0):
                LOG.info("Successfully got Snapshot Schedule %s", obj_ss)
                return obj_ss
            else:
                msg = "Failed to get snapshot schedule " \
                      "with name {0}".format(name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        except Exception as e:
            msg = errormsg.format(name, str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def get_io_limit_policy(self, name=None, id=None):
        """Get the instance of a io limit policy.
            :param name: The io limit policy name
            :param id: The io limit policy id
            :return: instance of the respective io_limit_policy if exist.
        """

        errormsg = "Failed to get the io limit policy {0} with error {1}"
        id_or_name = name if name else id

        try:
            obj_iopol = self.unity_conn.get_io_limit_policy(_id=id, name=name)
            if id and obj_iopol.existed:
                LOG.info("Successfully got the IO limit policy object %s",
                         obj_iopol)
                return obj_iopol
            elif name:
                LOG.info("Successfully got the IO limit policy object %s ",
                         obj_iopol)
                return obj_iopol
            else:
                msg = "Failed to get the io limit policy with {0}".format(
                    id_or_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        except Exception as e:
            msg = errormsg.format(name, str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def get_pool(self, pool_name=None, pool_id=None):
        """Get the instance of a pool.
            :param pool_name: The name of the pool
            :param pool_id: The id of the pool
            :return: Dict containing pool details if exists
        """

        id_or_name = pool_id if pool_id else pool_name
        errormsg = "Failed to get the pool {0} with error {1}"

        try:
            obj_pool = self.unity_conn.get_pool(name=pool_name, _id=pool_id)

            if pool_id and obj_pool.existed:
                LOG.info("Successfully got the pool object %s",
                         obj_pool)
                return obj_pool
            if pool_name:
                LOG.info("Successfully got pool %s", obj_pool)
                return obj_pool
            else:
                msg = "Failed to get the pool with " \
                      "{0}".format(id_or_name)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        except Exception as e:
            msg = errormsg.format(id_or_name, str(e))
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def get_NodeEnum_enum(self, sp):
        """Get the storage processor enum.
             :param sp: The storage processor string
             :return: storage processor enum
        """

        if sp in utils.NodeEnum.__members__:
            return utils.NodeEnum[sp]
        else:
            errormsg = "Invalid choice {0} for storage processor".format(
                sp)
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def get_tiering_policy_enum(self, tiering_policy):
        """Get the tiering_policy enum.
             :param tiering_policy: The tiering_policy string
             :return: tiering_policy enum
        """

        if tiering_policy in utils.TieringPolicyEnum.__members__:
            return utils.TieringPolicyEnum[tiering_policy]
        else:
            errormsg = "Invalid choice {0} for tiering policy".format(
                tiering_policy)
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def create_volume(self, obj_pool, size, host_access=None):
        """Create a volume.
            :param obj_pool: pool object instance
            :param size: size of the volume in GB
            :param host_access: host to be associated with this volume
            :return: Volume object on successful creation
        """

        vol_name = self.module.params['vol_name']

        try:

            description = self.module.params['description']
            compression = self.module.params['compression']
            is_thin = self.module.params['is_thin']
            snap_schedule = None

            sp = self.module.params['sp']
            sp = self.get_NodeEnum_enum(sp) if sp else None

            io_limit_policy = self.get_io_limit_policy(
                id=self.param_io_limit_pol_id) \
                if self.module.params['io_limit_policy'] else None

            if self.param_snap_schedule_name:
                snap_schedule = {"name": self.param_snap_schedule_name}

            tiering_policy = self.module.params['tiering_policy']
            tiering_policy = self.get_tiering_policy_enum(tiering_policy) \
                if tiering_policy else None

            obj_vol = obj_pool.create_lun(lun_name=vol_name,
                                          size_gb=size,
                                          sp=sp,
                                          host_access=host_access,
                                          is_thin=is_thin,
                                          description=description,
                                          tiering_policy=tiering_policy,
                                          snap_schedule=snap_schedule,
                                          io_limit_policy=io_limit_policy,
                                          is_compression=compression)

            LOG.info("Successfully created volume , %s", obj_vol)

            return obj_vol

        except Exception as e:
            errormsg = "Create volume operation {0} failed" \
                       " with error {1}".format(vol_name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def host_access_modify_required(self, host_access_list):
        """Check if host access modification is required
            :param host_access_list: host access dict list
            :return: Dict with attributes to modify, or None if no
            modification is required.
        """

        try:
            to_modify = False
            hlu = self.module.params['hlu']
            mapping_state = self.module.params['mapping_state']

            host_id_list = []
            hlu_list = []
            for host_access in host_access_list.host:
                host_id_list.append(host_access.id)
                host = self.get_host(host_id=host_access.id).update()
                host_dict = host.host_luns._get_properties()
                LOG.debug("check if hlu present : %s", host_dict)
                if "hlu" in host_dict.keys():
                    hlu_list.append(host_dict['hlu'])

            LOG.debug("Host Dictionaries:- host_id: %s, hlu: %s",
                      host_id_list, hlu_list)

            if mapping_state == 'mapped':
                if (self.param_host_id not in host_id_list):
                    # <hlu list not available in API response> or (hlu not in hlu_list):
                    to_modify = True

            if mapping_state == 'unmapped':
                if (self.param_host_id in host_id_list):
                    # <hlu list not available in API response> or (hlu in hlu_list):
                    to_modify = True

            LOG.debug("host_access_modify_required : %s ", str(to_modify))
            return to_modify

        except Exception as e:
            errormsg = "Failed to compare the host_access with error {0} " \
                       "{1}".format(host_access_list, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def volume_modify_required(self, obj_vol, cap_unit):
        """Check if volume modification is required
            :param obj_vol: volume instance
            :param cap_unit: capacity unit
            :return: Boolean value to indicate if modification is required
        """

        try:
            to_update = {}

            new_vol_name = self.module.params['new_vol_name']
            if new_vol_name and obj_vol.name != new_vol_name:
                to_update.update({'name': new_vol_name})

            description = self.module.params['description']
            if description and obj_vol.description != description:
                to_update.update({'description': description})

            size = self.module.params['size']
            if size and cap_unit:
                size_byte = int(utils.get_size_bytes(size, cap_unit))
                if size_byte < obj_vol.size_total:
                    self.module.fail_json(msg="Volume size can be "
                                              "expanded only")
                elif size_byte > obj_vol.size_total:
                    to_update.update({'size': size_byte})

            compression = self.module.params['compression']
            if compression is not None and \
                    compression != obj_vol.is_data_reduction_enabled:
                to_update.update({'is_compression': compression})

            is_thin = self.module.params['is_thin']
            if is_thin is not None and is_thin != obj_vol.is_thin_enabled:
                self.module.fail_json(msg="Modifying is_thin is not allowed")

            sp = self.module.params['sp']
            if sp and self.get_NodeEnum_enum(sp) != obj_vol.current_node:
                to_update.update({'sp': self.get_NodeEnum_enum(sp)})

            tiering_policy = self.module.params['tiering_policy']
            if tiering_policy and self.get_tiering_policy_enum(
                    tiering_policy) != obj_vol.tiering_policy:
                to_update.update({'tiering_policy':
                                  self.get_tiering_policy_enum(
                                      tiering_policy)})

            # prepare io_limit_policy object
            if self.param_io_limit_pol_id:
                if (not obj_vol.io_limit_policy) \
                        or (self.param_io_limit_pol_id
                            != obj_vol.io_limit_policy.id):
                    to_update.update(
                        {'io_limit_policy': self.param_io_limit_pol_id})

            # prepare snap_schedule object
            if self.param_snap_schedule_name:
                if (not obj_vol.snap_schedule) \
                        or (self.param_snap_schedule_name
                            != obj_vol.snap_schedule.name):
                    to_update.update({'snap_schedule':
                                      self.param_snap_schedule_name})

            #  for removing existing snap_schedule
            if self.param_snap_schedule_name == "":
                if obj_vol.snap_schedule:
                    to_update.update({'is_snap_schedule_paused': False})
                else:
                    LOG.warn("No snapshot schedule is associated")

            LOG.debug("Volume to modify  Dict : %s", to_update)
            if len(to_update) > 0:
                return to_update
            else:
                return None

        except Exception as e:
            errormsg = "Failed to determine if volume {0},requires " \
                       "modification, with error {1}".format(obj_vol.name,
                                                             str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def attach_to(self, host, obj_vol, hlu=None):
        """Attach/map a host/hlu to a volume
        :param host: host to map the volume
        :param obj_vol: volume instance
        :param hlu: hlu to map the volume
        :return: None on successful modification
        """
        try:
            resp = obj_vol.attach_to(host, hlu=hlu)
            return resp
        except Exception as e:
            errormsg = "Failed to attach host {0} with volume {1} ,  " \
                       "with error {2} ".format(host, obj_vol.name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def detach_from(self, host, obj_vol):
        """Detach/unmap a host from a volume
        :param host: host to map the volume
        :param obj_vol: volume instance
        :return: response from API call
        """

        try:
            resp = obj_vol.detach_from(host)
            return resp
        except Exception as e:
            errormsg = "Detach host {0} from volume {1} operation failed " \
                       "with error {2}".format(host, obj_vol.name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def modify_volume(self, obj_vol, to_modify_dict):
        """modify volume attributes
            :param obj_vol: volume instance
            :param to_modify_dict: dict containing attributes to be modified.
            :return: None
        """

        try:

            if 'io_limit_policy' in to_modify_dict.keys():
                to_modify_dict['io_limit_policy'] = self.get_io_limit_policy(
                    id=to_modify_dict['io_limit_policy'])

            if 'snap_schedule' in to_modify_dict.keys() and \
                    to_modify_dict['snap_schedule'] != "":
                to_modify_dict['snap_schedule'] = \
                    {"name": to_modify_dict['snap_schedule']}

            param_list = ['name', 'size', 'host_access', 'description', 'sp',
                          'io_limit_policy', 'tiering_policy',
                          'snap_schedule', 'is_snap_schedule_paused',
                          'is_compression']

            for item in param_list:
                if item not in to_modify_dict.keys():
                    to_modify_dict.update({item: None})

            LOG.debug("Final update dict before modify "
                      "api call: %s", to_modify_dict)

            obj_vol.modify(name=to_modify_dict['name'],
                           size=to_modify_dict['size'],
                           host_access=to_modify_dict['host_access'],
                           description=to_modify_dict['description'],
                           sp=to_modify_dict['sp'],
                           io_limit_policy=to_modify_dict['io_limit_policy'],
                           tiering_policy=to_modify_dict['tiering_policy'],
                           snap_schedule=to_modify_dict['snap_schedule'],
                           is_snap_schedule_paused=to_modify_dict[
                               'is_snap_schedule_paused'],
                           is_compression=to_modify_dict['is_compression'])

        except Exception as e:
            errormsg = "Failed to modify the volume {0} " \
                       "with error {1}".format(obj_vol.name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def delete_volume(self, vol_id):
        """Delete volume.
        :param vol_obj: The object instance of the volume to be deleted
        """

        try:
            obj_vol = self.get_volume(vol_id=vol_id)
            obj_vol.delete(force_snap_delete=False)
            return True

        except Exception as e:
            errormsg = "Delete operation of volume id:{0} " \
                       "failed with error {1}".format(id,
                                                      str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def get_volume_display_attributes(self, obj_vol):
        """get display volume attributes
        :param obj_vol: volume instance
        :return: volume dict to display
        """
        try:
            obj_vol = obj_vol.update()
            volume_details = obj_vol._get_properties()
            volume_details['size_total_with_unit'] = utils. \
                convert_size_with_unit(int(volume_details['size_total']))
            host_list = []
            if obj_vol.host_access:
                for host_access in obj_vol.host_access:
                    host = self.get_host(host_id=host_access.host.id).update()
                    host_dict = host.host_luns._get_properties()
                    host_list.append({'name': host_access.host.name,
                                      'id': host_access.host.id,
                                      'hlu': host_dict['hlu']})
            volume_details.update({'host_access': host_list})
            if obj_vol.snap_schedule:
                volume_details.update(
                    {'snap_schedule': {'name': obj_vol.snap_schedule.name,
                                       'id': obj_vol.snap_schedule.id}})
            if obj_vol.io_limit_policy:
                volume_details.update(
                    {'io_limit_policy': {'name': obj_vol.io_limit_policy.id,
                                         'id': obj_vol.io_limit_policy.id}})
            if obj_vol.pool:
                volume_details.update({'pool': {'name': obj_vol.pool.name,
                                                'id': obj_vol.pool.id}})

            return volume_details

        except Exception as e:
            errormsg = "Failed to display the volume {0} with " \
                       "error {1}".format(obj_vol.name, str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def validate_input_string(self):
        """ validates the input string checks if it's empty string """
        invalid_string = ""
        try:
            no_chk_list = ['snap_schedule', 'description']
            for key in self.module.params:
                val = self.module.params[key]
                if key not in no_chk_list and isinstance(val, str) \
                        and val == invalid_string:
                    errmsg = 'Invalid input parameter "" for {0}'.format(
                        key)
                    self.module.fail_json(msg=errmsg)

        except Exception as e:
            errormsg = "Failed to validate the module param with " \
                       "error {0}".format(str(e))
            LOG.error(errormsg)
            self.module.fail_json(msg=errormsg)

    def perform_module_operation(self):
        """
        Perform different actions on volume module based on parameters
        passed in the playbook
        """
        vol_name = self.module.params['vol_name']
        vol_id = self.module.params['vol_id']
        pool_name = self.module.params['pool_name']
        pool_id = self.module.params['pool_id']
        size = self.module.params['size']
        cap_unit = self.module.params['cap_unit']
        snap_schedule = self.module.params['snap_schedule']
        io_limit_policy = self.module.params['io_limit_policy']
        host_name = self.module.params['host_name']
        host_id = self.module.params['host_id']
        hlu = self.module.params['hlu']
        mapping_state = self.module.params['mapping_state']
        new_vol_name = self.module.params['new_vol_name']
        state = self.module.params['state']

        # result is a dictionary to contain end state and volume details
        changed = False
        result = dict(
            changed=False,
            volume_details=None
        )

        to_modify_dict = None
        volume_details = None
        to_modify_host = False

        self.validate_input_string()

        if size is not None and size == 0:
            self.module.fail_json(msg="Size can not be 0 (Zero)")

        if size and not cap_unit:
            cap_unit = 'GB'

        if (cap_unit is not None) and not size:
            self.module.fail_json(msg="cap_unit can be specified along "
                                      "with size")

        if hlu and (not host_name and not host_id):
            self.module.fail_json(msg="hlu can be specified with "
                                      "host_id or host_name")
        if mapping_state and (not host_name and not host_id):
            self.module.fail_json(msg="mapping_state can be specified"
                                      " with host_id or host_name")

        obj_vol = self.get_volume(vol_id=vol_id, vol_name=vol_name)

        if host_name or host_id:
            if not mapping_state:
                errmsg = "'mapping_state' is required along with " \
                         "'host_name' or 'host_id'"
                self.module.fail_json(msg=errmsg)
            host = self.get_host(host_id=host_id, host_name=host_name)
            self.param_host_id = host.id if host else None

        if io_limit_policy:
            io_limit_policy = self.get_io_limit_policy(name=io_limit_policy)
            self.param_io_limit_pol_id = io_limit_policy.id

        if snap_schedule:
            snap_schedule = self.get_snap_schedule(name=snap_schedule)
            self.param_snap_schedule_name = snap_schedule.name[0]

        # this is for removing existing snap_schedule
        if snap_schedule == "":
            self.param_snap_schedule_name = snap_schedule

        if obj_vol:
            volume_details = obj_vol._get_properties()
            vol_id = obj_vol.get_id()
            to_modify_dict = self.volume_modify_required(obj_vol, cap_unit)
            LOG.debug("Volume Modify Required: %s", to_modify_dict)
            if obj_vol.host_access:
                to_modify_host = self.host_access_modify_required(
                    host_access_list=obj_vol.host_access)
                LOG.debug("Host Modify Required: %s", to_modify_host)
            elif self.param_host_id:
                to_modify_host = True
                LOG.debug("Host Modify Required: %s", to_modify_host)

        if state == 'present' and not volume_details:
            if not vol_name:
                msg_noname = "volume with id {0} is not found, unable to " \
                             "create a volume without a valid " \
                             "vol_name".format(vol_id)
                self.module.fail_json(msg=msg_noname)

            if snap_schedule == "":
                self.module.fail_json(msg="Invalid snap_schedule")

            if new_vol_name:
                self.module.fail_json(msg="new_vol_name is not required "
                                          "to create a new volume")
            if not pool_name and not pool_id:
                self.module.fail_json(msg="pool_id or pool_name is required "
                                          "to create new volume")
            if not size:
                self.module.fail_json(msg="Size is required to create"
                                          " a volume")
            host_access = None
            if self.param_host_id:
                host = self.get_host(host_id=self.param_host_id)
                if hlu:
                    host_access = [
                        {'host': host,
                         'accessMask': utils.HostLUNAccessEnum.PRODUCTION,
                         'hlu': hlu}]
                else:
                    host_access = [
                        {'host': host,
                         'accessMask': utils.HostLUNAccessEnum.PRODUCTION}]

            size = utils.get_size_in_gb(size, cap_unit)

            obj_pool = self.get_pool(pool_name=pool_name, pool_id=pool_id)

            obj_vol = self.create_volume(obj_pool=obj_pool, size=size,
                                         host_access=host_access)
            LOG.debug("Successfully created volume , %s", obj_vol)
            vol_id = obj_vol.id
            volume_details = obj_vol._get_properties()
            LOG.debug("Got volume id , %s", vol_id)
            changed = True

        if state == 'present' and volume_details and to_modify_dict:
            self.modify_volume(obj_vol=obj_vol, to_modify_dict=to_modify_dict)
            changed = True

        if (state == 'present' and volume_details
                and mapping_state == 'mapped' and to_modify_host):
            host = self.get_host(host_id=self.param_host_id)
            resp = self.attach_to(host=host, hlu=hlu, obj_vol=obj_vol)
            changed = True if resp else False

        if (state == 'present' and volume_details
                and mapping_state == 'unmapped' and to_modify_host):
            host = self.get_host(host_id=self.param_host_id)
            resp = self.detach_from(host=host, obj_vol=obj_vol)
            changed = True if resp else False

        if state == 'absent' and volume_details:
            changed = self.delete_volume(vol_id)
            volume_details = None

        if state == 'present' and volume_details:
            volume_details = self.get_volume_display_attributes(
                obj_vol=obj_vol)

        result['changed'] = changed
        result['volume_details'] = volume_details
        self.module.exit_json(**result)


def get_unity_volume_parameters():
    """This method provide parameters required for the ansible volume
       module on Unity"""
    return dict(
        vol_name=dict(required=False, type='str'),
        vol_id=dict(required=False, type='str'),
        description=dict(required=False, type='str'),
        pool_name=dict(required=False, type='str'),
        pool_id=dict(required=False, type='str'),
        size=dict(required=False, type='int'),
        cap_unit=dict(required=False, type='str', choices=['GB', 'TB']),
        is_thin=dict(required=False, type='bool', default=True),
        compression=dict(required=False, type='bool'),
        sp=dict(required=False, type='str', choices=['SPA', 'SPB']),
        io_limit_policy=dict(required=False, type='str'),
        snap_schedule=dict(required=False, type='str'),
        host_name=dict(required=False, type='str'),
        host_id=dict(required=False, type='str'),
        hlu=dict(required=False, type='int'),
        mapping_state=dict(required=False, type='str',
                           choices=['mapped', 'unmapped']),
        new_vol_name=dict(required=False, type='str'),
        tiering_policy=dict(required=False, type='str', choices=[
            'AUTOTIER_HIGH', 'AUTOTIER', 'HIGHEST', 'LOWEST']),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """ Create Unity volume object and perform action on it
        based on user input from playbook"""
    obj = UnityVolume()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
