#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myproject.api
# import myproject.db

def list_opts():
    return [
        ('api', myproject.api.OPTS),
        # ('database', myproject.db.OPTS),
    ]