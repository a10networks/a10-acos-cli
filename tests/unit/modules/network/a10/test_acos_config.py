# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, A10 Networks Inc.
# GNU General Public License v3.0
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from mock import MagicMock, Mock
import os

from ansible_collections.a10.acos_cli.plugins.modules import acos_config
from ansible_collections.a10.acos_cli.plugins.cliconf.acos import Cliconf
from ansible_collections.a10.acos_cli.tests.unit.compat.mock import patch
from ansible_collections.a10.acos_cli.tests.unit.modules.utils import AnsibleFailJson
from ansible_collections.a10.acos_cli.tests.unit.modules.utils import set_module_args
from ansible_collections.a10.acos_cli.tests.unit.modules.network.a10.base import (
    TestAcosModule, load_fixture)


class TestAcosConfigModule(TestAcosModule):

    module = acos_config

    def setUp(self):
        super(TestAcosConfigModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.a10.acos_cli.plugins.modules.acos_config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_get_connection = patch(
            "ansible_collections.a10.acos_cli.plugins.modules.acos_config.get_connection"
        )
        self.get_connection = self.mock_get_connection.start()

        self.conn = self.get_connection()
        self.conn.edit_config = MagicMock()
        self.conn.get_diff = MagicMock()

        self.mock_run_commands = patch(
            "ansible_collections.a10.acos_cli.plugins.modules.acos_config.run_commands"
        )
        self.run_commands = self.mock_run_commands.start()

<<<<<<< HEAD
<<<<<<< HEAD
        self.src = os.path.join(os.path.dirname(
=======
        self.file_path = os.path.join(os.path.dirname(
>>>>>>> Modified UTs for backup and src
=======
        self.src = os.path.join(os.path.dirname(
>>>>>>> Update test_acos_config.py
            __file__), 'fixtures/show_config_file_commands.cfg')
        self.backup_spec = {
            "filename": "test_backup.cfg",
            "dir_path": "fixtures/backup/"
        }

        self.cliconf_obj = Cliconf(MagicMock())

        self.running_config = load_fixture("acos_running_config.cfg")
        self.match = 'line'
        self.diff_ignore_lines = 'none'

    def tearDown(self):
        super(TestAcosConfigModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_run_commands.stop()
        self.mock_get_connection.stop()

    def load_fixtures(self, filename=None):
        config_file = "acos_running_config.cfg"
        self.get_config.return_value = load_fixture(config_file)
        self.get_connection.edit_config.return_value = None

    def test_acos_config_lines(self):
        lines = ["ip dns primary 10.18.18.81"]
        set_module_args(dict(lines=lines))
        self.execute_module()
        self.conn.get_diff = MagicMock(
            return_value=self.cliconf_obj.get_diff(
                candidate=lines, running=self.running_config, diff_match=self.match,
                diff_ignore_lines=self.diff_ignore_lines
            )
        )
        self.assertIn("ip dns primary 10.18.18.81",
                      self.conn.get_diff.return_value['config_diff'])
        self.assertTrue(self.conn.edit_config.called)

    def test_acos_config_multi_lines(self):
        lines = ["ip dns primary 10.18.18.81", "member rs1-test 80",
                 "slb server server2-test 5.5.5.11"]
        set_module_args(dict(lines=lines))
        self.execute_module()
        self.conn.get_diff = MagicMock(
            return_value=self.cliconf_obj.get_diff(
                candidate=lines, running=self.running_config, diff_match=self.match,
                diff_ignore_lines=self.diff_ignore_lines
            )
        )
        self.assertIn("ip dns primary 10.18.18.81",
                      self.conn.get_diff.return_value['config_diff'])
        self.assertIn("member rs1-test 80",
                      self.conn.get_diff.return_value['config_diff'])
        self.assertIn("slb server server2-test 5.5.5.11",
                      self.conn.get_diff.return_value['config_diff'])
        self.assertTrue(self.conn.edit_config.called)

    def test_acos_config_before(self):
        lines = ["ip dns primary 10.18.18.19"]
        set_module_args(dict(lines=lines, before=["show avcs"]))
        self.execute_module()
        commands = ["show avcs", "ip dns primary 10.18.18.19"]
        self.conn.get_diff = MagicMock(
            return_value=self.cliconf_obj.get_diff(
                candidate=commands, running=self.running_config, diff_match=self.match,
                diff_ignore_lines=self.diff_ignore_lines
            )
        )
        self.assertIn("ip dns primary 10.18.18.19",
                      self.conn.get_diff.return_value['config_diff'])
        self.assertIn(
            "show avcs", self.conn.get_diff.return_value['config_diff'])
        self.assertTrue(self.conn.edit_config.called)

    def test_acos_config_after(self):
        lines = ["ip dns primary 10.18.18.19"]
        set_module_args(dict(lines=lines, after=["show avcs"]))
        self.execute_module()
        commands = ["ip dns primary 10.18.18.19", "show avcs"]
        self.conn.get_diff = MagicMock(
            return_value=self.cliconf_obj.get_diff(
                candidate=commands, running=self.running_config, diff_match=self.match,
                diff_ignore_lines=self.diff_ignore_lines
            )
        )
        self.assertIn("ip dns primary 10.18.18.19",
                      self.conn.get_diff.return_value['config_diff'])
        self.assertIn(
            "show avcs", self.conn.get_diff.return_value['config_diff'])
        self.assertTrue(self.conn.edit_config.called)

    def test_acos_config_save_changed_false(self):
        set_module_args(dict(save_when="changed"))
        self.execute_module()
        self.assertEqual(self.run_commands.call_count, 3)
        self.assertEqual(self.conn.edit_config.call_count, 0)
        args = self.run_commands.call_args_list
        commands = [x[0][1] for x in args]
        self.assertNotIn("write memory\r", commands)

    def test_acos_config_save_always(self):
        lines = ["ip dns primary 10.18.18.19"]
        set_module_args(dict(lines=lines, save_when="always"))
        self.execute_module()
        self.assertEqual(self.run_commands.call_count, 4)
        self.assertEqual(self.conn.edit_config.call_count, 1)
        args = self.run_commands.call_args_list
        commands = [x[0][1] for x in args]
        self.assertIn("write memory\r", commands)

    @patch("ansible_collections.a10.acos_cli.plugins.modules.acos_config.NetworkConfig")
    def test_acos_config_save_no_modified(self, mock_networkConfig):
        lines = ["ip dns primary 10.18.18.39"]
        set_module_args(dict(lines=lines, save_when="modified"))
        self.execute_module()

        args = self.run_commands.call_args_list[-1][0][1]
        self.assertEqual(args, ['show running-config', 'show startup-config'])

        self.assertEqual(mock_networkConfig.call_count, 3)

        commands = [x[0][1] for x in self.run_commands.call_args_list]
        self.assertNotIn("write memory\r", commands)

    @patch("ansible_collections.a10.acos_cli.plugins.modules.acos_config.NetworkConfig")
    def test_acos_config_save_modified(self, mock_networkConfig):

        running_config_fixture = Mock()
        running_config_fixture.sha1 = "show running_config fixtures"
        startup_config_fixture = Mock()
        startup_config_fixture.sha1 = "show startup_config fixtures"

        mock_networkConfig.side_effect = [
            running_config_fixture, startup_config_fixture]
        set_module_args(dict(save_when="modified"))

        self.execute_module()
        args = self.run_commands.call_args_list

        commands = [x[0][1] for x in args]
        self.assertIn("write memory\r", commands)

    def test_acos_config_src(self):
        set_module_args(dict(src=self.src))
        self.execute_module()
        self.assertTrue(self.conn.edit_config.called)

    def test_acos_config_backup(self):
        set_module_args(dict(backup=True))
        result = self.execute_module()
        self.assertIn("__backup__", result)

    @patch("ansible_collections.a10.acos_cli.plugins.modules.acos_config.run_commands")
    def test_acos_config_in_existing_partition(self, mock_partition):
        fixture = [load_fixture("acos_config_show_partition.cfg")]
        mock_partition.return_value = fixture
        partition_name = 'my_partition'
        set_module_args(dict(partition=partition_name))
        self.execute_module()
        second_args = [calls[0][1]
                       for calls in mock_partition.call_args_list]
        self.assertIn('active-partition my_partition', second_args)

    @patch("ansible_collections.a10.acos_cli.plugins.modules.acos_config.run_commands")
    def test_acos_config_partition_does_not_exist(self, mock_partition):
        fixture = [load_fixture(
            "acos_config_active-partition_my_partition3.cfg")]
        mock_partition.return_value = fixture
        partition_name = 'my_partition3'
        set_module_args(dict(partition=partition_name))
        self.assertRaises(AnsibleFailJson, self.execute_module)
        with self.assertRaises(AnsibleFailJson):
            result = self.execute_module()
            self.assertIn('Provided partition does not exist', result['msg'])

    def test_acos_config_match_exact(self):
        lines = ["ip dns primary 10.18.18.81"]
        set_module_args(dict(lines=lines, match="exact"))
        self.execute_module()
        self.conn.get_diff.assert_called_with(
            candidate='ip dns primary 10.18.18.81', diff_ignore_lines=None,
            diff_match='exact', running=self.running_config)

    def test_acos_config_match_strict(self):
        lines = ["ip dns primary 10.18.18.81"]
        set_module_args(dict(lines=lines, match="strict"))
        self.execute_module()
        self.conn.get_diff.assert_called_with(
            candidate='ip dns primary 10.18.18.81', diff_ignore_lines=None,
            diff_match='strict', running=self.running_config)

    def test_acos_config_match_none(self):
        lines = ["ip dns primary 10.18.18.81"]
        set_module_args(dict(lines=lines, match="none"))
        self.execute_module()
        self.conn.get_diff.assert_called_with(
            candidate='ip dns primary 10.18.18.81', diff_ignore_lines=None,
            diff_match='none', running=self.running_config)
