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
from openstackclient.common import utils as oscutils

from ironicclient.common.i18n import _
from ironicclient import exc
from ironicclient.v1 import resource_fields as res_fields


class ListBaremetal(lister.Lister):
    """List baremetal nodes"""

    log = logging.getLogger(__name__ + ".ListBaremetal")

    def get_parser(self, prog_name):
        parser = super(ListBaremetal, self).get_parser(prog_name)
        parser.add_argument(
            "--matching",
            metavar="<hostname>",
            help="Filter hypervisors using <hostname> substring",
        )
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help='Maximum number of nodes to return per request, '
                 '0 for no limit. Default is the maximum number used '
                 'by the Baremetal API Service.'
        )
        parser.add_argument(
            '--marker',
            metavar='<node>',
            help='Node UUID (for example, of the last node in the list from '
                 'a previous request). Returns the list of nodes after this '
                 'UUID.'
        )
        parser.add_argument(
            '--sort',
            metavar="<key>[:<direction>]",
            help='Sort output by selected keys and directions(asc or desc) '
                 '(default: asc), multiple keys and directions can be '
                 'specified separated by comma',
        )
        parser.add_argument(
            '--maintenance',
            dest='maintenance',
            action='store_true',
            default=False,
            help="List nodes in maintenance mode.",
        )
        parser.add_argument(
            '--associated',
            dest='associated',
            action='store_true',
            default=False,
            help="List nodes by instance association."
        )
        parser.add_argument(
            '--detail',
            dest='detail',
            action='store_true',
            default=False,
            help="Show detailed information about the nodes."
        )
        parser.add_argument(
            '--long',
            dest='detail',
            action='store_true',
            default=False,
            help="Show detailed information about the nodes. "
                 "Alias for --detail.",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.baremetal

        columns = tuple(res_fields.NODE_LIST_FIELD_LABELS)

        params = {}
        if parsed_args.limit is not None:
            if parsed_args.limit < 0:
                raise exc.CommandError(
                    _('Expected non-negative --limit, got %s') %
                    parsed_args.limit)
            params['limit'] = parsed_args.limit
        params['marker'] = parsed_args.marker
        params['associated'] = parsed_args.associated
        params['maintenance'] = parsed_args.maintenance

        if parsed_args.detail:
            columns = tuple(res_fields.NODE_FIELD_LABELS)
        params['detail'] = parsed_args.detail

        data = client.node.list(**params)

        data = oscutils.sort_items(data, parsed_args.sort)

        column_headers = columns

        return (column_headers,
                (oscutils.get_item_properties(s, columns, formatters={
                    'Properties': oscutils.format_dict},) for s in data))
