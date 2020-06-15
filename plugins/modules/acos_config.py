#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, A10 Networks Inc.
# GNU General Public License v3.0
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: acos_config
short_description: Manage A10 ACOS device configuration
description:
  - A10 ACOS configurations use a simple block indent file syntax
    for segmenting configuration into sections.  This module provides
    an implementation for working with ACOS configuration sections.
version_added: '2.9'
author: Hunter Thompson (@hthompson6)
notes:
  - Tested against ACOS 4.1.1-P9
  - Abbreviated commands are NOT idempotent, see
    L(Network FAQ,../network/user_guide/faq.html#why-do-the-config-modules-
      always-return-changed-true-with-abbreviated-commands).
options:
  lines:
    description:
      - The ordered set of commands that should be configured in the
        section.  The commands must be the exact same commands as found
        in the device running-config.  Be sure to note the configuration
        command syntax as some commands are automatically modified by the
        device config parser.
    aliases: ['commands']
  intended_config:
    description:
      - The ordered set of commands that is checked with the commands given
        under lines. The intended set is compared with 'lines' set. The
        intended commands that is not part of line commands set are
        returned.
  src:
    description:
      - Specifies the source path to the file that contains the configuration
        or configuration template to load.  The path to the source file can
        either be the full path on the Ansible control host or a relative
        path from the playbook or role root directory.
  backup:
    description:
      - This argument will cause the module to create a full backup of
        the current C(running-config) from the remote device before any
        changes are made. If the C(backup_options) value is not given,
        the backup file is written to the C(backup) folder in the playbook
        root directory or role root directory, if playbook is part of an
        ansible role. If the directory does not exist, it is created.
    type: bool
    default: 'no'
  defaults:
    description:
      - This argument specifies whether or not to collect all defaults
        when getting the remote device running config.  When enabled,
        the module will get the current config by issuing the command
        C(show running-config all).
    type: bool
    default: 'no'
  before:
    description:
      - The ordered set of commands to push on to the command stack if
        a change needs to be made.  This allows the playbook designer
        the opportunity to perform configuration commands prior to pushing
        any changes without affecting how the set of commands are matched
        against the system.
  after:
    description:
      - The ordered set of commands to append to the end of the command
        stack if a change needs to be made.  Just like with I(before) this
        allows the playbook designer to append a set of commands to be
        executed after the command set.
  diff_ignore_lines:
    description:
      - Use this argument to specify one or more lines that should be ignored
        while running the check between running config and lines sets. This
        is used for lines in the configuration that are automatically updated
        by the system. This argument takes a list of commands.
  save_when:
    description:
      - When changes are made to the device running-configuration, the
        changes are not copied to non-volatile storage by default.  Using
        this argument will change that before.  If the argument is set to
        I(always), then the running-config will always be copied to the
        startup-config and the I(modified) flag will always be set to
        True.  If the argument is set to I(modified), then the running-config
        will only be copied to the startup-config if it has changed since
        the last save to startup-config.  If the argument is set to
        I(never), the running-config will never be copied to the
        startup-config.  If the argument is set to I(changed), then the
        running-config will only be copied to the startup-config if the task
        has made a change.
    default: never
    choices: ['always', 'never', 'modified', 'changed']
  backup_options:
    description:
      - This is a dict object containing configurable options related to
        backup file path.
        The value of this option is read only when C(backup) is set to I(yes),
        if C(backup) is set to I(no) this option will be silently ignored.
    suboptions:
      filename:
        description:
          - The filename to be used to store the backup configuration. If the
            filename is not given it will be generated based on the hostname,
            current time and date in format defined by
            <hostname>_config.<current-date>@<current-time>
      dir_path:
        description:
          - This option provides the path ending with directory name in which
            the backup configuration file will be stored. If the directory
            does not exist it will be first created and the filename is either
            the value of C(filename) or default filename as described in
            C(filename) options description. If the path value is not given in
            that case a I(backup) directory will be created in the current
            working directory and backup configuration will be copied in
            C(filename) within I(backup) directory.
        type: path
    type: dict
  diff_against:
    description:
      - Possible value is 'startup'. Provides output as difference between
        running config and startup config. Configuration set that is part of
        startup config but not part of running config is returned.
    choices: ['running', 'startup', 'intended']
  partition:
    description:
      - This argument is used to specify the partition name on which you want to
        execute configurations in a task. This option activates the provided
        partition and performs given configurations on it.
    default: shared
'''

EXAMPLES = r'''
- name: simple loadbalancer create commands
  a10.acos_cli.acos_config:
    lines:
      - ip dns primary 8.8.4.7
      - slb template http slb-http-test
      - slb server server1-test 6.6.5.6
      - port 80 tcp
      - slb server server2-test 5.5.5.11
      - port 80 tcp
      - slb service-group sgtest-1 tcp
      - member rs1-test 80
      - member rs2-test 80
      - slb virtual-server viptest1 2.2.2.3
      - port 80 http

- name: render a template onto an ACOS device
  a10.acos_cli.acos_config:
    backup: yes
    src: config.cfg

- name: configure from multiple files
  a10.acos_cli.acos_config:
    src: "{{item}}"
  register: _result
  loop:
    - file1.cfg
    - file2.cfg

- name: save running to startup when modified
  a10.acos_cli.acos_config:
    save_when: modified

- name: configurable backup path
  a10.acos_cli.acos_config:
    default: true
    backup: yes
    backup_options:
      filename: backup.cfg
      dir_path: /home/user

- name: run lines with check_mode
  a10.acos_cli.acos_config:
    lines:
      - ip dns primary 10.10.10.55
      - slb template http abc-config
  check_mode: yes

- name: run lines on my_partition
  a10.acos_cli.acos_config:
    partition: 'my_partition'
    lines:
      - slb template http test_template1
      - slb server test_server1 10.10.21.44
'''

RETURN = r'''
updates:
  description: The set of commands that will be pushed to the remote device
  returned: always
  type: list
  sample: ['hostname foo', 'router ospf 1', 'router-id 192.0.2.1']
commands:
  description: The set of commands that will be pushed to the remote device
  returned: always
  type: list
  sample: ['hostname foo', 'router ospf 1', 'router-id 192.0.2.1']
backup_path:
  description: The full path to the backup file
  returned: when backup is yes
  type: str
  sample: /playbooks/ansible/backup/acos_config.2016-07-16@22:28:34
filename:
  description: The name of the backup file
  returned: when backup is yes and filename is not specified in backup options
  type: str
  sample: acos_config.2020-07-16@22:28:34
shortname:
  description: The full path to the backup file excluding the timestamp
  returned: when backup is yes and filename is not specified in backup options
  type: str
  sample: /playbooks/ansible/backup/acos_config
date:
  description: The date extracted from the backup file name
  returned: when backup is yes
  type: str
  sample: "2020-07-16"
time:
  description: The time extracted from the backup file name
  returned: when backup is yes
  type: str
  sample: "22:28:34"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.a10.acos_cli.plugins.module_utils.network.a10.acos import (
    get_config, run_commands, get_connection)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import (
    NetworkConfig, dumps)


def get_candidate_config(module):
    candidate = ''
    if module.params['src']:
        candidate = module.params['src']
    elif module.params['lines']:
        candidate_obj = NetworkConfig(indent=1)
        candidate_obj.add(module.params['lines'])
        candidate = dumps(candidate_obj, 'raw')
    return candidate


def get_intended_config(module):
    intended_lines = module.params['intended_config']
    intended_obj_list = list()
    for line in intended_lines:
        intended_obj_list.append(str(line.strip()))
    return intended_obj_list


def get_list_from_params(command_lines):
    candidate_obj_list = list()
    if command_lines:
        for line in command_lines:
            candidate_obj_list.append(str(line.strip()))
    return candidate_obj_list


def save_config(module):
    if not module.check_mode:
        run_commands(module, 'write memory\r')
    else:
        module.warn('Skipping command `write memory` '
                    'due to check_mode.  Configuration not copied to '
                    'non-volatile storage')


def configuration_to_list(configuration):
    sanitized_config_list = list()
    config_list = configuration[0].split('\n')
    for line in config_list:
        if not line.startswith('!'):
            sanitized_config_list.append(line.strip())
    return sanitized_config_list


def main():
    """ main entry point for module execution
    """
    backup_spec = dict(
        filename=dict(),
        dir_path=dict(type='path')
    )
    argument_spec = dict(
        src=dict(type='path'),
        lines=dict(aliases=['commands'], type='list'),
        intended_config=dict(aliases=['commands'], type='list'),
        before=dict(type='list'),
        after=dict(type='list'),
        defaults=dict(type='bool', default=False),
        backup=dict(type='bool', default=False),
        backup_options=dict(type='dict', options=backup_spec),
        save_when=dict(choices=['always', 'never', 'modified', 'changed'],
                       default='never'),
        diff_against=dict(choices=['startup']),
        diff_ignore_lines=dict(type='list'),
        partition=dict(default='shared')

    )

    mutually_exclusive = [("lines", "src")]

    module = AnsibleModule(argument_spec=argument_spec,
                           mutually_exclusive=mutually_exclusive,
                           supports_check_mode=True)

    connection = get_connection(module)

    result = {'changed': False}

    warnings = list()

    if module.params['partition'].lower() != 'shared':
        partition_name = module.params['partition']
        out = run_commands(module, 'active-partition %s' % (partition_name))
        if "does not exist" in str(out[0]):
            module.fail_json(msg="Provided partition does not exist")

    diff_ignore_lines = module.params['diff_ignore_lines']
    contents = None
    flags = 'with-default' if module.params['defaults'] else []

    startup_config_list = configuration_to_list(run_commands(module,
                                                             'show running-config'))

    if module.params['backup'] or (module._diff and
                                   module.params['diff_against'] == 'running'):
        contents = get_config(module, flags=flags)
        if module.params['backup']:
            result['__backup__'] = contents

    if any((module.params['lines'], module.params['src'])):
        candidate = get_candidate_config(module)

        config_diff = candidate

        if config_diff:
            commands = config_diff.splitlines()

            if module.params['before']:
                commands[:0] = module.params['before']

            if module.params['after']:
                commands.extend(module.params['after'])

            result['commands'] = commands
            result['updates'] = commands

            # send the configuration commands to the device and merge
            # them with the current running config
            if not module.check_mode:
                if commands:
                    connection.edit_config(candidate=commands)
                    result['changed'] = True

    # for comparing running config with candidate config
    running_config_list = configuration_to_list(run_commands(module,
                                                             'show running-config'))

    candidate_lines = get_list_from_params(module.params['lines'])
    diff_ignore_lines_list = get_list_from_params(diff_ignore_lines)
    difference = connection.get_diff(intended_config=candidate_lines,
                                     candidate_config=running_config_list,
                                     diff_ignore_lines=diff_ignore_lines_list)
    if len(difference) != 0:
        module.warn('Could not execute following commands or command does not'
                    ' exist in running config after execution. check'
                    'on ACOS device:' + str(difference))

    # intended_config
    if module.params['intended_config']:
        intended_config_list = get_intended_config(module)
        found_diff = connection.get_diff(intended_config_list, candidate_lines,
                                         diff_ignore_lines_list)
        if len(found_diff) != 0:
            result.update({
                'success': False,
                'failed_diff_lines_between_intended_candidate': found_diff
            })
        else:
            result.update({
                'success': True
            })

    after_config_list = configuration_to_list(run_commands(module,
                                                           'show running-config'))
    diff = list(set(after_config_list) - set(startup_config_list))
    if len(diff) != 0:
        result['changed'] = True
    else:
        result['changed'] = False

    if module.params['save_when'] == 'always':
        save_config(module)
    elif module.params['save_when'] == 'modified':
        output = run_commands(module,
                              ['show running-config', 'show startup-config'])
        running_config = NetworkConfig(indent=1, contents=output[0],
                                       ignore_lines=diff_ignore_lines)
        startup_config = NetworkConfig(indent=1, contents=output[1],
                                       ignore_lines=diff_ignore_lines)
        if running_config.sha1 != startup_config.sha1:
            save_config(module)

    elif module.params['save_when'] == 'changed' and result['changed']:
        save_config(module)

    if module.params['diff_against'] == 'startup':
        difference_with_startup_config = connection.get_diff(startup_config_list,
                                                             running_config_list,
                                                             diff_ignore_lines_list)
        if len(difference_with_startup_config) != 0:
            result.update({
                'diff_against_found': 'yes',
                'changed': True,
                'startup_diff': difference_with_startup_config
            })
        else:
            result.update({
                'diff_against_found': 'no',
                'changed': False,
                'startup_diff': None
            })

    result['warnings'] = warnings
    module.exit_json(**result)


if __name__ == '__main__':
    main()
