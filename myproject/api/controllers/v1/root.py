#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from myproject.api.controllers.v1 import students as v1Students

class V1Controller(rest.RestController):
    """Version 1 API controller root."""

    students = v1Students.StudentsController()

    @wsme_pecan.wsexpose(wtypes.text)
    def get(self):
        return '#######  V1Controller'