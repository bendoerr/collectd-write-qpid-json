import collectd
import sys
from qpid.messaging import *


def handle_config(config):
    host = [it for it in config.children if it.key == 'Host']
    collectd.info('%s' % host)


def handle_write(vl):
    collectd.info('cake, %s' % vl)




collectd.register_config(handle_config)
collectd.register_init(handle_init)
