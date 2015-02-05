import collectd
import write_common


################################################################################
# Globals
################################################################################


#
# Name of this plugin for logging
#
plugin_name = 'write_log_json'

#
# Default configuration values
#
config = {
    'TypesDB': ['/usr/share/collectd/types.db']
}

#
# Parsed types.db values
#
types = {}


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

    # If we made it this far, go ahead and register the write plugin
    collectd.register_write(handle_write)
    collectd.info(
        '%s: Initialized and registered write handler.' % plugin_name)


def handle_write(vl):
    collectd.info(write_common.value_to_json(vl, types))


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



