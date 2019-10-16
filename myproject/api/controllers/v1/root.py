#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from myproject.api.controllers.v1 import students as v1Students
from myproject.api.controllers.v1 import rpc as v1Rpc

class V1Controller(rest.RestController):
    """Version 1 API controller root."""

    students = v1Students.StudentsController()
    rpc = v1Rpc.RpcController()

    @wsme_pecan.wsexpose(wtypes.text)
    def get(self):
        return '#######  V1Controller'