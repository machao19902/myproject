#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oslo_config import cfg
from oslo_log import log
from oslo_db import options as db_options

from myproject import opts

def prepareService(argv=None, configFile=None):
    conf= cfg.ConfigOpts()
    log.register_options(conf)
    log.set_defaults(default_log_levels=conf.default_log_levels)
    db_options.set_defaults(conf)
    for group, options in opts.list_opts():
        conf.register_opts(
            group=group if group else 'DEFAULT', opts=list(options))
    conf(argv,
         project='myproject',
         validate_default_values=True,
         default_config_files=configFile)
    log.setup(conf, 'myproject')
    return conf
