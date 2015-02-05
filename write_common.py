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
from string import lower


#
# Parse types.db file
#
def parse_types_db(paths, plugin_name):
    local_types = {}
    for path in paths:
        fh = open(path, 'r')
        for line in fh:
            fields = line.split()

            # Skip empty lines
            if len(fields) < 2:
                continue

            type_name = fields[0]

            # Skip comment lines
            if type_name[0] == '#':
                continue

            v = []
            for ds in fields[1:]:
                ds = ds.rstrip(',')
                ds_fields = ds.split(':')
                if len(ds_fields) != 4:
                    collectd.warning('%s: cannot parse types.db %s on %s' % (
                        plugin_name, ds, type_name))
                    continue
                v.append(ds_fields)
            local_types[type_name] = v
        fh.close()
    return local_types


def value_to_json(vl, types):
    # class Values(PluginData)
    # |  A Values object used for dispatching values to collectd and receiving values from write callbacks.
    # |
    # |  Method resolution order:
    # |      Values
    # |      PluginData
    #  |      __builtin__.object
    #  |
    #  |  Methods defined here:
    #  |
    #  |  __init__(...)
    #  |      x.__init__(...) initializes x; see help(type(x)) for signature
    #  |
    #  |  __repr__(...)
    #  |      x.__repr__() <==> repr(x)
    #  |
    #  |  dispatch(...)
    #  |      dispatch([type][, values][, plugin_instance][, type_instance][, plugin][, host][, time][, interval]) -> None.  Dispatch a value list.
    #  |
    #  |      Dispatch this instance to the collectd process. The object has members
    #  |      for each of the possible arguments for this method. For a detailed explanation
    #  |      of these parameters see the member of the same same.
    #  |
    #  |      If you do not submit a parameter the value saved in its member will be submitted.
    #  |      If you do provide a parameter it will be used instead, without altering the member.
    #  |
    #  |  write(...)
    #  |      write([destination][, type][, values][, plugin_instance][, type_instance][, plugin][, host][, time][, interval]) -> None.  Dispatch a value list.
    #  |
    #  |      Write this instance to a single plugin or all plugins if 'destination' is obmitted.
    #  |      This will bypass the main collectd process and all filtering and caching.
    #  |      Other than that it works similar to 'dispatch'. In most cases 'dispatch' should be
    #  |      used instead of 'write'.
    #  |
    #  |  ----------------------------------------------------------------------
    #  |  Data descriptors defined here:
    #  |
    #  |  interval
    #  |      The interval is the timespan in seconds between two submits for
    #  |      the same data source. This value has to be a positive integer, so you can't
    #  |      submit more than one value per second. If this member is set to a
    #  |      non-positive value, the default value as specified in the config file will
    #  |      be used (default: 10).
    #  |
    #  |      If you submit values more often than the specified interval, the average
    #  |      will be used. If you submit less values, your graphs will have gaps.
    #  |
    #  |  meta
    #  |      These are the meta data for this Value object.
    #  |      It has to be a dictionary of numbers, strings or bools. All keys must be
    #  |      strings. int and long objects will be dispatched as signed integers unless
    #  |      they are between 2**63 and 2**64-1, which will result in a unsigned integer.
    #  |      You can force one of these storage classes by using the classes
    #  |      collectd.Signed and collectd.Unsigned. A meta object received by a write
    #  |      callback will always contain Signed or Unsigned objects.
    #  |
    #  |  values
    #  |      These are the actual values that get dispatched to collectd.
    #  |      It has to be a sequence (a tuple or list) of numbers.
    #  |      The size of the sequence and the type of its content depend on the type
    #  |      member your types.db file. For more information on this read the types.db
    #  |      man page.
    #  |
    #  |      If the sequence does not have the correct size upon dispatch a RuntimeError
    #  |      exception will be raised. If the content of the sequence is not a number,
    #  |      a TypeError exception will be raised.
    #  |
    #  |  ----------------------------------------------------------------------
    #  |  Data and other attributes defined here:
    #  |
    #  |  __new__ = <built-in method __new__ of type object>
    #  |      T.__new__(S, ...) -> a new object with type S, a subtype of T
    #  |
    #  |  ----------------------------------------------------------------------
    #  |  Data descriptors inherited from PluginData:
    #  |
    #  |  host
    #  |      The hostname of the host this value was read from.
    #  |      For dispatching this can be set to an empty string which means
    #  |      the local hostname as defined in the collectd.conf.
    #  |
    #  |  plugin
    #  |      The name of the plugin that read the data. Setting this
    #  |      member to an empty string will insert "python" upon dispatching.
    #  |
    #  |  plugin_instance
    #  |
    #  |  time
    #  |      This is the Unix timestap of the time this value was read.
    #  |      For dispatching values this can be set to 0 which means "now".
    #  |      This means the time the value is actually dispatched, not the time
    #  |      it was set to 0.
    #  |
    #  |  type
    #  |      The type of this value. This type has to be defined
    #  |      in your types.db. Attempting to set it to any other value will
    #  |      raise a TypeError exception.
    #  |      Assigning a type is mandetory, calling dispatch without doing
    #  |      so will raise a RuntimeError exception.
    #  |
    #  |  type_instance

    # Example
    # collectd.Values(type='swap_io',type_instance='in',plugin='swap',host='edge-1',time=1423075370.9574316,interval=10.0,values=[0])
    # collectd.Values(type='if_packets',plugin='interface',plugin_instance='eth0',host='edge-1',time=1423075490.939849,interval=10.0,values=[750192, 381487])
    #  {
    #   "values":  [1901474177],
    #   "dstypes":  ["counter"],
    #   "dsnames":    ["value"],
    #   "time":      1280959128,
    #   "interval":          10,
    #   "host":            "leeloo.octo.it",
    #   "plugin":          "cpu",
    #   "plugin_instance": "0",
    #   "type":            "cpu",
    #   "type_instance":   "idle"
    # }

    this_type = types[vl.type]
    values_str = '[' + ','.join(map(str, vl.values)) + ']'
    dsnames_str = '[' + ','.join(
        '"%s"' % lower(it[0]) for it in this_type) + ']'
    dstypes_str = '[' + ','.join(
        '"%s"' % lower(it[1]) for it in this_type) + ']'

    return '{{"values":{values},"dstypes":{dstypes},"dsnames":{dsnames},"time":{time},"interval":{interval},"host":"{host}","plugin":"{plugin}","plugin_instance":"{plugin_instance}","type":"{type}","type_instance":"{type_instance}"}}'.format(
        values=values_str, dsnames=dsnames_str, dstypes=dstypes_str,
        time=vl.time, interval=vl.interval, host=vl.host, plugin=vl.plugin,
        plugin_instance=vl.plugin_instance, type=vl.type,
        type_instance=vl.type_instance)

#
# Merge a dictionary of keys and default values with collectd's Config object
# Doesn't support multiple value options right now.
#
def merge_configs(config, given_config, plugin_name):
    for key in config:
        given_values = [it for it in given_config.children if it.key == key]

        if not given_values:
            continue

        if isinstance(config[key], list):
            config[key] = [it.values for it in given_values][0]
        else:
            config[key] = given_values[0].values[0]

    return config
