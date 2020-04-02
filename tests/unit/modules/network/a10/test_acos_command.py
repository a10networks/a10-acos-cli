# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, A10 Networks Inc.
# GNU General Public License v3.0
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json

from ansible_collections.a10.acos_collection.plugins.modules import acos_command
from ansible_collections.a10.acos_collection.tests.unit.compat.mock import patch
from ansible_collections.a10.acos_collection.tests.unit.modules.utils import set_module_args
from ansible_collections.a10.acos_collection.tests.unit.modules.network.a10.base import (
    TestAcosModule, load_fixture)


class TestAcosCommandModule(TestAcosModule):

    module = acos_command

    def setUp(self):
        super(TestAcosCommandModule, self).setUp()

        self.mock_run_commands = patch(
            'ansible_collections.a10.acos_collection.plugins.modules.acos_command.run_commands')

        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestAcosCommandModule, self).tearDown()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None):

        def load_from_file(*args, **kwargs):
            module, commands = args
            output = []
            if isinstance(commands, str):
                filename = 'acos_command_' + str(commands).replace(' ', '_')
                output.append(load_fixture(filename))
                return output

            for item in commands:
                try:
                    obj = json.loads(item['command'])
                    command = obj['command']
                except ValueError:
                    command = item['command']
                filename = 'acos_command_' + str(command).replace(' ', '_')
                output.append(load_fixture(filename))
            return output

        self.run_commands.side_effect = load_from_file

    def test_acos_command_simple(self):
        set_module_args(dict(commands=['show version']))
        result = self.execute_module()
        self.assertTrue(result['stdout'][0].startswith('Thunder Series'))
        self.assertFalse(result['stdout'][0].startswith('ACOS'))
        self.assertIn('aFleX version: 2.0.0', result['stdout'][0])
        self.assertEqual(len(result['stdout']), 1)

    def test_acos_command_multiple(self):
        set_module_args(dict(commands=['show version', 'show hardware']))
        result = self.execute_module()
        self.assertIsNotNone(result['stdout'][0])
        self.assertEqual(len(result['stdout']), 2)
        self.assertTrue(result['stdout'][0].startswith('Thunder Series'))
        self.assertNotEqual(result['stdout'][0], "test")
        self.assertIsNotNone(result['stdout'][1])
        self.assertIn('Storage', result['stdout'][1])

    def test_acos_command_wait_for(self):
        wait_for = 'result[0] contains "ACOS"'
        set_module_args(dict(commands=['show version'], wait_for=wait_for))
        result = self.execute_module()
        self.assertIn('ACOS', result['stdout'][0])

    def test_acos_command_wait_for_fails(self):
        wait_for = 'result[0] contains "test"'
        set_module_args(dict(commands=['show version'], wait_for=wait_for))
        self.execute_module(failed=True)
        self.assertEqual(self.run_commands.call_count, 12)

    def test_acos_command_retries(self):
        wait_for = 'result[0] contains "ACOS"'
        set_module_args(
            dict(commands=['show version'], wait_for=wait_for, retries=2))
        self.execute_module()

    def test_acos_command_retries_failure(self):
        wait_for = 'result[0] contains "test"'
        set_module_args(
            dict(commands=['show version'], wait_for=wait_for, retries=2))
        self.execute_module(failed=True)

    def test_acos_command_match_any(self):
        wait_for = ['result[0] contains "Thunder"',
                    'result[0] contains "test"']
        set_module_args(
            dict(commands=['show version'], wait_for=wait_for, match='any'))
        self.execute_module()

    def test_acos_command_match_any_failure(self):
        wait_for = ['result[0] contains "test1"',
                    'result[0] contains "test2"']
        set_module_args(
            dict(commands=['show version'], wait_for=wait_for, match='any'))
        self.execute_module(failed=True)

    def test_acos_command_match_all(self):
        wait_for = ['result[0] contains "Thunder"',
                    'result[0] contains "ACOS"']
        set_module_args(
            dict(commands=['show version'], wait_for=wait_for, match='all'))
        self.execute_module()

    def test_acos_command_match_all_failure(self):
        wait_for = ['result[0] contains "Thunder"',
                    'result[0] contains "test"']
        commands = ['show version', 'show version']
        set_module_args(
            dict(commands=commands, wait_for=wait_for, match='all'))
        self.execute_module(failed=True)

    def test_acos_command_configure_check_warning(self):
        commands = ['configure']
        set_module_args({
            'commands': commands,
            '_ansible_check_mode': True,
        })
        result = self.execute_module()
        self.assertEqual(
            result['warnings'],
            ['Only show commands are supported when using check mode, not executing configure'],
        )

    def test_acos_command_configure_no_warning(self):
        commands = ['configure']
        set_module_args({
            'commands': commands,
            '_ansible_check_mode': True,
        })
        result = self.execute_module()
        self.assertNotEqual(result['warnings'], [])
