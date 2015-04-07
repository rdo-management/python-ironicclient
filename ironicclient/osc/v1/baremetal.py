# -*- coding: utf-8 -*-
#
#   Copyright 2015 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import logging

from cliff import lister


class ListBaremetal(lister.Lister):
    """List baremetal nodes"""

    log = logging.getLogger(__name__ + ".ListBaremetal")

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.baremetal

        columns = (
            "UUID",
            "Instance UUID",
            "Power State",
            "Provisioning State",
            "Maintenance"
        )
        data = client.node.list()

        return (
            columns,
            list((node.uuid, node.instance_uuid, node.power_state,
                  node.provision_state, node.maintenance)
                 for node in data)
        )
