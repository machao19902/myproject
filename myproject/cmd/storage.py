#!/usr/bin/env python
# -*- coding: utf-8 -*-

from myproject import service
from myproject import db

def dbsync():
    conf = service.prepareService()
    db.getConnectionFromConfig(conf).upgrade()