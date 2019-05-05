#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

import six

@six.add_metaclass(abc.ABCMeta)
class Connection(object):

    def __init__(self, conf, url):
        pass

    def upgrade(self):
        """ Migrate database """

    def getStudents(self):
        """ Get student list """

    def createStudent(self):
        """ Create a student"""

    def updateStudent(self):
        """  Update a student"""

    def deleteStudent(self):
        """ Delere a student """
