# -*- coding: utf-8 -*-
#
# Copyright: ©2024 A10 Networks, Inc. All rights reserved.

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
