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

from openstackclient.common import exceptions
from openstackclient.common import utils

from ironicclient.osc import client as ironic_client

LOG = logging.getLogger(__name__)

DEFAULT_BAREMETAL_API_VERSION = '1.6'
API_VERSION_OPTION = 'os_baremetal_api_version'
API_NAME = 'baremetal'
API_VERSION_MAP = {
    "1": "1",
    "1.6": "1",
}
API_VERSIONS = {
    '1': 'ironicclient.osc.client',
    '1.6': 'ironicclient.osc.client'
}


def make_client(instance):
    """Returns a baremetal service client."""
    try:
        baremetal_client = ironic_client.get_client_class(
            API_VERSION_MAP[instance._api_version[API_NAME]])
    except Exception:
        msg = "Invalid %s client version '%s'. Must be one of %s" % (
            (API_NAME, instance._api_version[API_NAME],
                ", ".join(sorted(API_VERSION_MAP))))
        raise exceptions.UnsupportedVersion(msg)
    LOG.debug('Instantiating baremetal client: %s', baremetal_client)

    # Set client http_log_debug to True if verbosity level is high enough
    http_log_debug = LOG.isEnabledFor(logging.DEBUG)

    extensions = []

    client = baremetal_client(
        session=instance.session,
        extensions=extensions,
        http_log_debug=http_log_debug,
        timings=instance.timing,
        region_name=instance._region_name,
    )

    return client


def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        '--os-baremetal-api-version',
        metavar='<baremetal-api-version>',
        default=utils.env(
            'OS_BAREMETAL_API_VERSION',
            default=DEFAULT_BAREMETAL_API_VERSION),
        help='Baremetal API version, default=' +
             DEFAULT_BAREMETAL_API_VERSION +
             ' (Env: OS_BAREMETAL_API_VERSION)')
    return parser
