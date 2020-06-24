# -*- coding: utf-8 -*-
#
# Copyright: (c) 2020, A10 Networks Inc.
# GNU General Public License v3.0
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible_collections.ansible.netcommon.plugins.action.network import (
    ActionModule as ActionNetworkModule,
)


class ActionModule(ActionNetworkModule):

    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect
        module_name = self._task.action.split(".")[-1]
        self._config_module = True if module_name == "acos_config" else False

        result = super(ActionModule, self).run(task_vars=task_vars)
        return result
