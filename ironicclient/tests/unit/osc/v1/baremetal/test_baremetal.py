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

import copy

from ironicclient.osc.v1 import baremetal
from ironicclient.tests.unit.osc import fakes
from ironicclient.tests.unit.osc.v1.baremetal import fakes as baremetal_fakes


class TestBaremetal(baremetal_fakes.TestBaremetal):

    def setUp(self):
        super(TestBaremetal, self).setUp()

        # Get a shortcut to the FlavorManager Mock
        self.baremetal_mock = self.app.client_manager.baremetal
        self.baremetal_mock.reset_mock()


class FakeBaremetalResource(fakes.FakeResource):

    def get_keys(self):
        return {'property': 'value'}


class TestBaremetalList(TestBaremetal):

    def setUp(self):
        super(TestBaremetalList, self).setUp()

        self.baremetal_mock.node.list.return_value = [
            FakeBaremetalResource(
                None,
                copy.deepcopy(baremetal_fakes.BAREMETAL),
                loaded=True,
            ),
        ]

        # Get the command object to test
        self.cmd = baremetal.ListBaremetal(self.app, None)

    def test_baremetal_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'associated': False,
            'detail': False,
            'maintenance': False,
            'marker': None,
        }

        self.baremetal_mock.node.list.assert_called_with(
            **kwargs
        )

        collist = (
            "UUID",
            "Name",
            "Instance UUID",
            "Power State",
            "Provisioning State",
            "Maintenance"
        )
        self.assertEqual(collist, columns)
        datalist = ((
            baremetal_fakes.baremetal_uuid,
            '',
            baremetal_fakes.baremetal_instance_uuid,
            baremetal_fakes.baremetal_power_state,
            '',
            baremetal_fakes.baremetal_maintenance,
        ), )
        self.assertEqual(datalist, tuple(data))

    def test_baremetal_list_long(self):
        arglist = [
            '--long',
        ]
        verifylist = [
            ('detail', True),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = {
            'associated': False,
            'detail': True,
            'maintenance': False,
            'marker': None,
        }

        self.baremetal_mock.node.list.assert_called_with(
            **kwargs
        )

        collist = ('Chassis UUID', 'Created At', 'Console Enabled', 'Driver',
                   'Driver Info', 'Driver Internal Info', 'Extra',
                   'Instance Info', 'Instance UUID', 'Last Error',
                   'Maintenance', 'Maintenance Reason', 'Power State',
                   'Properties', 'Provision State', 'Reservation',
                   'Target Power State', 'Target Provision State',
                   'Updated At', 'Inspection Finished At',
                   'Inspection Started At', 'UUID', 'Name')
        self.assertEqual(collist, columns)
        datalist = ((
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            baremetal_fakes.baremetal_instance_uuid,
            '',
            baremetal_fakes.baremetal_maintenance,
            '',
            baremetal_fakes.baremetal_power_state,
            '',
            baremetal_fakes.baremetal_provision_state,
            '',
            '',
            '',
            '',
            '',
            '',
            baremetal_fakes.baremetal_uuid,
            '',
        ), )
        self.assertEqual(datalist, tuple(data))
