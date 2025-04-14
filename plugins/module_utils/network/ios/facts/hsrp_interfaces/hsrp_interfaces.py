# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The ios hsrp_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.hsrp_interfaces.hsrp_interfaces import (
    Hsrp_interfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.rm_templates.hsrp_interfaces import (
    Hsrp_interfacesTemplate,
)


class Hsrp_interfacesFacts(object):
    """The ios hsrp_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Hsrp_interfacesArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Hsrp_interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = connection.get('sh running-config | section ^interface')

        # parse native config using the Hsrp_interfaces template
        hsrp_interfaces_parser = Hsrp_interfacesTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        objs = list(hsrp_interfaces_parser.parse().values())

        ansible_facts["ansible_network_resources"].pop("hsrp_interfaces", None)

        params = utils.remove_empties(
            hsrp_interfaces_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["hsrp_interfaces"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
