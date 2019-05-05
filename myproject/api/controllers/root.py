#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from myproject.api.controllers.v1 import root as v1

class RootController(rest.RestController):
    v1 = v1.V1Controller()

    @wsme_pecan.wsexpose(wtypes.text)
    def get(self):
        return "####### RootController"