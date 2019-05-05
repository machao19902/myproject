#!/usr/bin/env python
# -*- coding: utf-8 -*-

import retrying
import six.moves.urllib.parse as urlparse
from stevedore import driver

G_NAMESPACE = "myproject.storage"

def getConnectionFromConfig(conf):
    url = conf.database.connection
    connectionScheme = urlparse.urlparse(url).scheme
    mgr = driver.DriverManager(G_NAMESPACE, connectionScheme)
    retries = conf.database.max_retries

    @retrying.retry(wait_fixed=conf.database.retry_interval * 1000,
                    stop_max_attempt_number=retries if retries >= 0 else None)
    def getConnection():
        return mgr.driver(conf)

    connection = getConnection()
    return connection