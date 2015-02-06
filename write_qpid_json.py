# The MIT License (MIT)
#
# Copyright (c) 2015 Ben Doerr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import collectd
import write_common
from qpid.messaging import *

################################################################################
# Globals
################################################################################


#
# Name of this plugin for logging
#
plugin_name = 'write_qpid_json'

#
# Default configuration values
#
config = {
    'TypesDB': ['/usr/share/collectd/types.db'],
    'Host': 'localhost',
    'Port': '5672',
    'User': 'guest',
    'Password': 'guest',
    'Exchange': 'amq.fanout'
}

#
# Parsed types.db values
#
types = {}

#
# QPid Connection
#
connection = None


################################################################################
# Handlers
################################################################################


def handle_config(given_config):
    global config
    config = write_common.merge_configs(config, given_config, plugin_name)

    collectd.info('%s: Configured: %s' % (plugin_name, config))


def handle_init():
    global types
    types = write_common.parse_types_db(config['TypesDB'], plugin_name)

    # global connection
    # connection = Connection("%s/%s@%s:%s" % (
    #     config['User'], config['Password'], config['Host'], config['Port']))

    # If we made it this far, go ahead and register the write plugin
    collectd.register_write(handle_write)
    collectd.info(
        '%s: Initialized and registered write handler.' % plugin_name)


def handle_shutdown():
    if connection != None and connection.opened():
        try:
            connection.close()
            collectd.info("%s: Closed connection to endpoint." % plugin_name)
        except MessagingError,m:
            collectd.info("%s: Couldn't close connection." % plugin_name)

    if connection != None:
        connection = None


def handle_write(vl):
    global connection
    if connection == None:
        connection = Connection("%s/%s@%s:%s" % (
            config['User'], config['Password'], config['Host'], config['Port']))

    try:
        if not connection.opened():
            # Open the connection if needed.
            connection.open()
            collectd.info("%s: Opened connection to endpoint." % plugin_name)

        # Open a session
        session = connection.session()
        sender = session.sender(config['Exchange'])

        # Send the message
        sender.send(Message(write_common.value_to_json(vl, types)))

        # Close the session
        session.close()

    except ConnectionError,m:
        collectd.error("%s: Failed to connect - %s" % (plugin_name, m))
        connection = None

    except MessagingError,m:
        collectd.error("%s: Failed to send AMQP message - %s" % (plugin_name, m))
        handle_shutdown()

    except Error,m:
        collectd.error("%s: Unknown Error - %s" % (plugin_name, m))
        handle_shutdown()



################################################################################
# Register handlers
################################################################################

# register_config(...)
# register_config(callback[, data][, name]) -> identifier
#
# Register a callback function for config file entries.
#
#     'callback' is a callable object that will be called for every config block
#     'data' is an optional object that will be passed back to the callback
#         function every time it is called.
#     'name' is an optional identifier for this callback. The default name
#         is 'python.<module>'.
#         Every callback needs a unique identifier, so if you want to
#         register this callback multiple time from the same module you need
#         to specify a name here.
#     'identifier' is the full identifier assigned to this callback.
#
#     The callback function will be called with one or two parameters:
#     config: A Config object.
#     data: The optional data parameter passed to the register function.
#         If the parameter was omitted it will be omitted here, too.

collectd.register_config(handle_config)


# register_init(...)
# register_init(callback[, data][, name]) -> identifier
#
#     Register a callback function that will be executed once after the config.
#     file has been read, all plugins heve been loaded and the collectd has
#     forked into the background.
#
#     'callback' is a callable object that will be executed.
#     'data' is an optional object that will be passed back to the callback
#         function when it is called.
#     'name' is an optional identifier for this callback. The default name
#         is 'python.<module>'.
#         Every callback needs a unique identifier, so if you want to
#         register this callback multiple time from the same module you need
#         to specify a name here.
#     'identifier' is the full identifier assigned to this callback.
#
#     The callback function will be called without parameters, except for
#     data if it was supplied.

collectd.register_init(handle_init)


# register_write(...)
# register_write(callback[, data][, name]) -> identifier
#
#     Register a callback function to receive values dispatched by other plugins
#
#     'callback' is a callable object that will be called every time a value
#         is dispatched.
#     'data' is an optional object that will be passed back to the callback
#         function every time it is called.
#     'name' is an optional identifier for this callback. The default name
#         is 'python.<module>'.
#         Every callback needs a unique identifier, so if you want to
#         register this callback multiple time from the same module you need
#         to specify a name here.
#     'identifier' is the full identifier assigned to this callback.
#
#     The callback function will be called with one or two parameters:
#     values: A Values object which is a copy of the dispatched values.
#     data: The optional data parameter passed to the register function.
#         If the parameter was omitted it will be omitted here, too.

# collectd.register_write(handle_write) # Registered as part of handle_init

collectd.register_shutdown(handle_shutdown)

