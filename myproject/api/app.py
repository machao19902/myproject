#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from oslo_config import cfg
from oslo_log import log
from paste import deploy
import pecan

from myproject.api import hooks
from myproject import service
from myproject import db

PECAN_CONFIG = {
    'app': {
        'root': 'myproject.api.controllers.root.RootController',
        'modules': ['myproject.api'],
    },
}

LOG = log.getLogger(__name__)


def app_factory(global_config, **local_config):
    print "######### enter app_factory"
    conf = service.prepareService()

    # NOTE, add config and databse information to the request
    # by using pecan.hooks.PecanHook
    configHook = hooks.ConfigHook(conf)
    conn = db.getConnectionFromConfig(conf)
    databaseHook = hooks.DatabaseHook(conn)
    appHooks = [configHook, databaseHook]

    # NOTE, it needs add the line below
    pecan.configuration.set_config(dict(PECAN_CONFIG), overwrite=True)
    app = pecan.make_app(
        PECAN_CONFIG['app']['root'],
        hooks=appHooks
    )
    return app

def getUri(conf):
    # TODO(), it needs to get real path of api-paste.ini
    # the path is setted by the data_files under [files] in setup.config
    # configPath = "/etc/myproject/api-paste.ini"

    # find the absolute path of api-paste.ini
    cfgFile = None
    apiPastePath = conf.api.paste_config
    if not os.path.isabs(apiPastePath):
        cfgFile = conf.find_file(apiPastePath)
    elif os.path.exists(apiPastePath):
        cfgFile = apiPastePath
    if not cfgFile:
        raise cfg.ConfigFilesNotFoundError([conf.api.paste_config])
    LOG.info("The wsgi config file path is: %s" % (cfgFile))
    result = "config:" + cfgFile
    return result

def getAppName():
    return "main"

def build_wsgi_app():
    print "######### enter build_wsgi_app"
    conf = service.prepareService()
    uri = getUri(conf)
    appName = getAppName()
    app = deploy.loadapp(uri, name=appName)
    return app