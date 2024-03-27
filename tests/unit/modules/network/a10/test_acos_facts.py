# -*- coding: utf-8 -*-
#
# Copyright: ©2024 A10 Networks, Inc. All rights reserved.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.a10.acos_cli.plugins.modules import acos_facts
from ansible_collections.a10.acos_cli.tests.unit.compat.mock import patch
from ansible_collections.a10.acos_cli.tests.unit.modules.utils import AnsibleFailJson
from ansible_collections.a10.acos_cli.tests.unit.modules.utils import set_module_args
from ansible_collections.a10.acos_cli.tests.unit.modules.network.a10.base import (
    TestAcosModule, load_fixture)


class TestAcosFactsModule(TestAcosModule):

    module = acos_facts

    def setUp(self):
        super(TestAcosFactsModule, self).setUp()
        self.mock_run_commands = patch(
            'ansible_collections.a10.acos_cli.plugins.module_utils.network.a10.facts.base.run_commands')
        self.run_commands = self.mock_run_commands.start()

        self.mock_get_capabilities = patch(
            'ansible_collections.a10.acos_cli.plugins.module_utils.network.a10.facts.base.get_capabilities')
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {
            'device_info': {
                'network_os': 'acos',
                'network_os_image': '4.1.1-P9.105',
                'network_os_model': 'Thunder Series Unified Application Service Gateway vThunder',
                'network_os_version': '64-bit Advanced Core OS (ACOS) version 4.1.1-P9, build 105 (Sep-21-2018,22:25)'
            },
            'network_api': 'cliconf'
        }

    def tearDown(self):
        super(TestAcosFactsModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_get_capabilities.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            commands = kwargs['commands']
            output = []

            for command in commands:
                filename = str(command).replace(' | ', '_').replace(' ', '_')
                output.append(load_fixture('acos_facts_%s' % filename))
            return output

        self.run_commands.side_effect = load_from_file

    def test_acos_facts_default(self):
        set_module_args(dict(gather_subset='default'))
        result = self.execute_module()
        self.assertEqual(
            result['ansible_facts'][
                'ansible_net_hostid'], 'ABCDEFGHIJKLMNOPQ'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_image'], '4.1.1-P9.105'
        )
        self.assertEqual(
            result['ansible_facts'][
                'ansible_net_model'], 'Thunder Series Unified Application Service Gateway vThunder'
        )
        self.assertEqual(
            result['ansible_facts'][
                'ansible_net_version'], '64-bit Advanced Core OS (ACOS) version 4.1.1-P9, build 105 (Sep-21-2018,22:25)'
        )

    def test_acos_facts_hardware(self):
        set_module_args(dict(gather_subset='hardware'))
        result = self.execute_module()
        self.assertEqual(
            result['ansible_facts']['ansible_net_memfree_mb'], "3897 Mbyte"
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_memtotal_mb'], "8071 Mbyte"
        )

    def test_acos_facts_negation_hardware(self):
        set_module_args(dict(gather_subset='!hardware'))
        result = self.execute_module()
        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces'][
                'Ethernet 4']['operstatus'], 'up'
        )
        self.assertIsNotNone(
            result['ansible_facts'][
                'ansible_net_interfaces']['Ethernet 4']['duplex']
        )
        self.assertNotIn(
            'ansible_net_memfree_mb', result['ansible_facts']
        )
        self.assertNotIn(
            'ansible_net_memtotal_mb', result['ansible_facts']
        )

    def test_acos_facts_interfaces(self):
        set_module_args(dict(gather_subset='interfaces'))
        result = self.execute_module()
        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces'][
                'Ethernet 1']['mtu'], 1500
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces'][
                'Ethernet 2']['ipv6'][0]['address'], '2001:db8:85a3::8a2e:370:7334'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces'][
                'Ethernet 3']['macaddress'], 'fa16.3e6d.95ec'
        )
        self.assertIsNone(
            result['ansible_facts'][
                'ansible_net_interfaces']['lif 10']['duplex']
        )
        self.assertIsNotNone(
            result['ansible_facts'][
                'ansible_net_interfaces']['Ethernet 2']['duplex']
        )

    def test_acos_facts_config(self):
        set_module_args(dict(gather_subset='config'))
        result = self.execute_module()
        self.assertEqual(
            result['ansible_facts']['ansible_net_api'], 'cliConf'
        )
        self.assertNotEqual(
            result['ansible_facts']['ansible_net_serialnum'], '123'
        )
        self.assertNotIn(
            '!Current configuration:', result[
                'ansible_facts']['ansible_net_config']
        )

    @patch("ansible_collections.a10.acos_cli.plugins.modules.acos_facts.run_commands")
    def test_acos_facts_in_existing_partition(self, mock_partition):
        set_module_args(dict(partition='my_partition', gather_subset='config'))
        self.execute_module()
        second_args = [calls[0][1]
                       for calls in mock_partition.call_args_list]
        self.assertIn('active-partition my_partition', second_args)
        self.assertTrue(mock_partition.called)

    @patch("ansible_collections.a10.acos_cli.plugins.modules.acos_facts.run_commands")
    def test_acos_facts_partition_does_not_exist(self, mock_partition):
        fixture = [load_fixture("acos_facts_active-partition_my_partition_new")]
        mock_partition.return_value = fixture
        set_module_args(dict(partition='my_partition_new', gather_subset='config'))
        with self.assertRaises(AnsibleFailJson):
            result = self.execute_module()
            self.assertIn('Provided partition does not exist', result['msg'])
