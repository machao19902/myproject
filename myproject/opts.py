#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myproject.api
import myproject.cmd.polling

def list_opts():
    return [
        ('api', myproject.api.OPTS),
        ('polling', myproject.cmd.polling.OPTS),
    ]

