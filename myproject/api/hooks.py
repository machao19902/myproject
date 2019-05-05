#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pecan import hooks

class ConfigHook(hooks.PecanHook):
    """Attach config information to the request
    
    """
    def __init__(self, conf):
        self.conf = conf

    def before(self, state):
        state.request.cfg = self.conf


class DatabaseHook(hooks.PecanHook):
    """Attach database information to the request
    
    """
    def __init__(self, conn):
        self.storage = conn

    def before(self, state):
        state.request.storage = self.storage