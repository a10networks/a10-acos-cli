#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: ©2024 A10 Networks, Inc. All rights reserved.

from __future__ import (absolute_import, division, print_function)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = r'''
---
module: acos_facts
author: Hunter Thompson (@hthompson6), Omkar Telee (@OmkarTelee-A10),
        Afrin Chakure (@afrin-chakure-a10), Neha Kembalkar (@NehaKembalkarA10)
short_description: Collect facts from remote devices running A10 ACOS
description:
  - Collects a base set of device facts from a remote device that
    is running ACOS. This module prepends all of the
    base network fact keys with C(ansible_net_<fact>). The facts
    module will collect a base set of facts from the device
    and can enable or disable collection of additional facts.
version_added: '2.9'
options:
  gather_subset:
    description:
      - When supplied, this argument restricts the facts collected
         to a given subset.
      - Possible values for this argument include
         all, default, hardware, config and interfaces
      - Specify a list of comma seperated values (without spaces) to include
         a larger subset.
    required: false
    type: list
    default: 'all'
  partition:
    description:
      - This argument is used to specify the partition name from
        which you want to collect respective facts.
    type: str
    default: shared
notes:
  - Tested against ACOS 4.1.1-P9
'''

EXAMPLES = r'''
  tasks:
    - name: Collect all the facts
      a10.acos_cli.acos_facts:
        gather_subset: all

    - name: Collect only the config and default facts
      a10.acos_cli.acos_facts:
        gather_subset:
          - config

    - name: Do not collect hardware facts
      a10.acos_cli.acos_facts:
        gather_subset:
          - "!hardware"

    - name: Collect all the facts my_partition
      a10.acos_cli.acos_facts:
        partition: my_partition
        gather_subset: all
'''

RETURN = r'''
ansible_net_gather_subset:
  description: The list of fact subsets collected from the device
  returned: always
  type: list
ansible_net_model:
  description: The model name returned from the device
  returned: always
  type: str
ansible_net_hostid:
  description: The hostid returned from the device
  returned: always
  type: str
ansible_net_serialnum:
  description: The serial number of the remote device
  returned: always
  type: str
ansible_net_version:
  description: The operating system version running on the remote device
  returned: always
  type: str
ansible_net_image:
  description: The image file the device is running
  returned: always
  type: str
ansible_net_api:
  description: The name of the transport
  returned: always
  type: str
ansible_net_python_version:
  description: The Python version Ansible controller is using
  returned: always
  type: str

# hardware
ansible_net_memfree_mb:
  description: The available free memory on the remote device in Mb
  returned: when hardware is configured
  type: int
ansible_net_memtotal_mb:
  description: The total memory on the remote device in Mb
  returned: when hardware is configured
  type: int

# config
ansible_net_config:
  description: The current active config from the device
  returned: when config is configured
  type: str

# interfaces
ansible_net_all_ipv4_addresses:
  description: All IPv4 addresses configured on the device
  returned: when interfaces is configured
  type: list
ansible_net_all_ipv6_addresses:
  description: All IPv6 addresses configured on the device
  returned: when interfaces is configured
  type: list
ansible_net_interfaces:
  description: A hash of all interfaces running on the system
  returned: when interfaces is configured
  type: dict
'''

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.a10.acos_cli.plugins.module_utils.network.a10.acos import \
    run_commands
from ansible_collections.a10.acos_cli.plugins.module_utils.network.a10.facts.facts import \
    Facts


class FactsArgs(object):
    """ The arg spec for the acos_facts module """

    argument_spec = {
        'gather_subset': dict(default=['all'], type='list'),
        'partition': dict(default='shared')
    }


def main():
    """ Main entry point for AnsibleModule """
    argument_spec = FactsArgs.argument_spec

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    if module.params['partition'].lower() != 'shared':
        partition = module.params['partition']
        out = run_commands(module, 'active-partition %s' % (partition))
        if "does not exist" in str(out[0]):
            module.fail_json(msg="Provided partition does not exist")

    warnings = []
    ansible_facts, additional_warnings = Facts(module).get_facts()
    warnings.extend(additional_warnings)

    module.exit_json(ansible_facts=ansible_facts, warnings=warnings)


if __name__ == '__main__':
    main()
