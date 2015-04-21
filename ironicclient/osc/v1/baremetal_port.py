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

from cliff import show
import six

from ironicclient.common import utils


class CreateBaremetalPort(show.ShowOne):
    """Create a new port"""

    log = logging.getLogger(__name__ + ".CreateBaremetalPort")

    def get_parser(self, prog_name):
        parser = super(CreateBaremetalPort, self).get_parser(prog_name)

        parser.add_argument(
            'node_uuid',
            metavar='<node>',
            help='UUID of the node that this port belongs to.')
        parser.add_argument(
            'address',
            metavar='<address>',
            help='MAC address for this port.')
        parser.add_argument(
            '-e', '--extra',
            metavar="<key=value>",
            action='append',
            help="Record arbitrary key/value metadata. "
                 "Can be specified multiple times.")

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        baremetal_client = self.app.client_manager.baremetal

        field_list = ['address', 'extra', 'node_uuid']
        fields = dict((k, v) for (k, v) in vars(parsed_args).items()
                      if k in field_list and not (v is None))
        fields = utils.args_array_to_dict(fields, 'extra')
        port = baremetal_client.port.create(**fields)._info

        port.pop('links', None)

        return zip(*sorted(six.iteritems(port)))
