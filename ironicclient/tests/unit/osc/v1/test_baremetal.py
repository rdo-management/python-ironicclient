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
from ironicclient.tests.unit.osc.v1 import fakes as baremetal_fakes

from openstackclient.tests import utils as oscutils


class TestBaremetal(baremetal_fakes.TestBaremetal):

    def setUp(self):
        super(TestBaremetal, self).setUp()

        # Get a shortcut to the FlavorManager Mock
        self.baremetal_mock = self.app.client_manager.baremetal
        self.baremetal_mock.reset_mock()


class TestBaremetalList(TestBaremetal):

    def setUp(self):
        super(TestBaremetalList, self).setUp()

        self.baremetal_mock.node.list.return_value = [
            baremetal_fakes.FakeBaremetalResource(
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


class TestBaremetalShow(TestBaremetal):
    def setUp(self):
        super(TestBaremetalShow, self).setUp()

        self.baremetal_mock.node.get.return_value = (
            baremetal_fakes.FakeBaremetalResource(
                None,
                copy.deepcopy(baremetal_fakes.BAREMETAL),
                loaded=True,
            ))

        self.baremetal_mock.node.get_by_instance_uuid.return_value = (
            baremetal_fakes.FakeBaremetalResource(
                None,
                copy.deepcopy(baremetal_fakes.BAREMETAL),
                loaded=True,
            ))

        # Get the command object to test
        self.cmd = baremetal.ShowBaremetal(self.app, None)

    def test_baremetal_show(self):
        arglist = ['xxx-xxxxxx-xxxx']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        args = ['xxx-xxxxxx-xxxx']

        self.baremetal_mock.node.get.assert_called_with(
            *args
        )

        collist = (
            'instance_uuid',
            'maintenance',
            'power_state',
            'provision_state',
            'uuid'
        )
        self.assertEqual(collist, columns)
        datalist = (
            'yyy-yyyyyy-yyyy',
            False,
            None,
            None,
            'xxx-xxxxxx-xxxx'
        )
        self.assertEqual(datalist, tuple(data))

    def test_baremetal_show_with_instance_uuid(self):
        arglist = [
            'xxx-xxxxxx-xxxx',
            '--instance',
        ]

        verifylist = [
            ('instance_uuid', True)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        args = ['xxx-xxxxxx-xxxx']

        self.baremetal_mock.node.get_by_instance_uuid.assert_called_with(
            *args
        )


class TestBaremetalDelete(TestBaremetal):
    def setUp(self):
        super(TestBaremetalDelete, self).setUp()

        self.baremetal_mock.node.get.return_value = (
            baremetal_fakes.FakeBaremetalResource(
                None,
                copy.deepcopy(baremetal_fakes.BAREMETAL),
                loaded=True,
            ))

        # Get the command object to test
        self.cmd = baremetal.DeleteBaremetal(self.app, None)

    def test_baremetal_delete(self):
        arglist = ['xxx-xxxxxx-xxxx']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        # Set expected values
        args = ['xxx-xxxxxx-xxxx']

        self.baremetal_mock.node.delete.assert_called_with(
            *args
        )


class TestBaremetalCreate(TestBaremetal):
    def setUp(self):
        super(TestBaremetalCreate, self).setUp()

        self.baremetal_mock.node.create.return_value = (
            baremetal_fakes.FakeBaremetalResource(
                None,
                copy.deepcopy(baremetal_fakes.BAREMETAL),
                loaded=True,
            ))

        # Get the command object to test
        self.cmd = baremetal.CreateBaremetal(self.app, None)
        self.arglist = ['--driver', 'fake_driver']
        self.verifylist = [('driver', 'fake_driver')]
        self.collist = (
            'instance_uuid',
            'maintenance',
            'power_state',
            'provision_state',
            'uuid'
        )
        self.datalist = ('yyy-yyyyyy-yyyy', False, None, None,
                         'xxx-xxxxxx-xxxx')
        self.actual_kwargs = {
            'driver': 'fake_driver',
        }

    def check_with_options(self, addl_arglist, addl_verifylist, addl_kwargs):
        arglist = copy.copy(self.arglist) + addl_arglist
        verifylist = copy.copy(self.verifylist) + addl_verifylist

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        collist = copy.copy(self.collist)
        self.assertEqual(collist, columns)

        datalist = copy.copy(self.datalist)
        self.assertEqual(datalist, tuple(data))

        kwargs = copy.copy(self.actual_kwargs)
        kwargs.update(addl_kwargs)

        self.baremetal_mock.node.create.assert_called_once_with(**kwargs)

    def test_baremetal_create_no_options(self):
        arglist = []
        verifylist = []

        self.assertRaises(oscutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)

    def test_baremetal_create_with_driver(self):
        arglist = copy.copy(self.arglist)

        verifylist = copy.copy(self.verifylist)

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        collist = copy.copy(self.collist)
        self.assertEqual(collist, columns)

        datalist = copy.copy(self.datalist)
        self.assertEqual(datalist, tuple(data))

        kwargs = copy.copy(self.actual_kwargs)

        self.baremetal_mock.node.create.assert_called_once_with(**kwargs)

    def test_baremetal_create_with_chassis(self):
        self.check_with_options(['--chassis', 'chassis_uuid'],
                                [('chassis_uuid', 'chassis_uuid')],
                                {'chassis_uuid': 'chassis_uuid'})

    def test_baremetal_create_with_driver_info(self):
        self.check_with_options(['-i', 'arg1=val1', '-i', 'arg2=val2'],
                                [('driver_info',
                                  ['arg1=val1',
                                   'arg2=val2'])],
                                {'driver_info': {
                                    'arg1': 'val1',
                                    'arg2': 'val2'}})

    def test_baremetal_create_with_properties(self):
        self.check_with_options(['-p', 'arg1=val1', '-p', 'arg2=val2'],
                                [('properties',
                                  ['arg1=val1',
                                   'arg2=val2'])],
                                {'properties': {
                                    'arg1': 'val1',
                                    'arg2': 'val2'}})

    def test_baremetal_create_with_extra(self):
        self.check_with_options(['-e', 'arg1=val1', '-e', 'arg2=val2'],
                                [('extra',
                                  ['arg1=val1',
                                   'arg2=val2'])],
                                {'extra': {
                                    'arg1': 'val1',
                                    'arg2': 'val2'}})

    def test_baremetal_create_with_uuid(self):
        self.check_with_options(['--uuid', 'uuid'],
                                [('uuid', 'uuid')],
                                {'uuid': 'uuid'})

    def test_baremetal_create_with_name(self):
        self.check_with_options(['--name', 'name'],
                                [('name', 'name')],
                                {'name': 'name'})


class TestBaremetalReboot(TestBaremetal):
    def setUp(self):
        super(TestBaremetalReboot, self).setUp()

        # Get the command object to test
        self.cmd = baremetal.RebootBaremetal(self.app, None)

    def test_baremetal_reboot_no_options(self):
        arglist = []
        verifylist = []

        self.assertRaises(oscutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)

    def test_baremetal_set_uuid_only(self):
        arglist = ['node_uuid']
        verifylist = [('node', 'node_uuid')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.baremetal_mock.node.set_power_state.assert_called_once_with(
            'node_uuid', 'reboot')


class TestBaremetalPower(TestBaremetal):
    def setUp(self):
        super(TestBaremetalPower, self).setUp()

        # Get the command object to test
        self.cmd = baremetal.PowerBaremetal(self.app, None)

    def test_baremetal_reboot_no_options(self):
        arglist = []
        verifylist = []

        self.assertRaises(oscutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)

    def test_baremetal_power_uuid_only(self):
        arglist = ['node_uuid']
        verifylist = [('node', 'node_uuid')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.assertFalse(self.baremetal_mock.node.set_power_state.called)

    def test_baremetal_power_on(self):
        arglist = ['node_uuid', '--on']
        verifylist = [('node', 'node_uuid'),
                      ('on', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.baremetal_mock.node.set_power_state.assert_called_once_with(
            'node_uuid', 'on')

    def test_baremetal_power_off(self):
        arglist = ['node_uuid', '--off']
        verifylist = [('node', 'node_uuid'),
                      ('off', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        self.baremetal_mock.node.set_power_state.assert_called_once_with(
            'node_uuid', 'off')
