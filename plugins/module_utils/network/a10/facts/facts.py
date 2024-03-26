# -*- coding: utf-8 -*-
#
# Copyright: ©2024 A10 Networks, Inc. All rights reserved.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts import FactsBase
from ansible_collections.a10.acos_cli.plugins.module_utils.network.a10.facts.base import (
    Default, Hardware, Interfaces, Config)

FACT_LEGACY_SUBSETS = dict(
    default=Default,
    hardware=Hardware,
    interfaces=Interfaces,
    config=Config
)


class Facts(FactsBase):
    """ The fact class for ACOS """

    VALID_LEGACY_GATHER_SUBSETS = frozenset(FACT_LEGACY_SUBSETS.keys())

    def __init__(self, module):
        super(Facts, self).__init__(module)

    def get_facts(self, legacy_facts_type=None):
        """ Collects the facts for ACOS device
        :param legacy_facts_type: List of legacy facts types
        :param resource_facts_type: List of resource fact types
        :param data: previously collected conf
        :rtype: dict
        :return: the facts gathered
        """
        if self.VALID_LEGACY_GATHER_SUBSETS:
            self.get_network_legacy_facts(FACT_LEGACY_SUBSETS,
                                          legacy_facts_type)

        return self.ansible_facts, self._warnings
