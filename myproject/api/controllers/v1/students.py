#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oslo_log import log
import pecan
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan

from myproject.api.controllers.v1 import base
from myproject.api.controllers.v1 import utils

LOG = log.getLogger(__name__)

#class Student(wtypes.Base):
class Student(base.Base):
    def as_dict(self):
        return self.as_dict_from_keys(['id', 'userId', 'name',
                                       'age', 'email'])

    id = int
    userId = wtypes.wsattr(wtypes.text, mandatory=True)
    name = wtypes.text
    age = int
    email = wtypes.text


class Students(wtypes.Base):
    students = [Student]


class StudentController(rest.RestController):
    def __init__(self, id):
        self.id = id

    @wsmeext.pecan.wsexpose(Student)
    def get(self):
        students = list(pecan.request.storage.getStudents(id=self.id))
        if not students:
            raise 'Not Found student with id: %s' % (self.id)
        student = students[0]
        return student

    @wsmeext.pecan.wsexpose(Student, body=Student)
    def put(self, data):
        conn = pecan.request.storage
        data.id = int(self.id)
        student = conn.updateStudent(data)
        return student

    @wsmeext.pecan.wsexpose(None, status_code=204)
    def delete(self):
        pecan.request.storage.deleteStudent(self.id)
        info = "delete id: {id}".format(id=self.id)
        LOG.info(info)


class StudentsController(rest.RestController):
    @pecan.expose()
    def _lookup(self, id, *remainder):
        return StudentController(id), remainder

    @wsmeext.pecan.wsexpose([Student], [base.Query], [str], int, str)
    def get(self, q=None, sort=None, limit=None, marker=None):
        """Return all students, based on the query provided.

        :param q: Filter rules for the alarms to be returned.
        :param sort: A list of pairs of sort key and sort dir.
        :param limit: The maximum number of items to be return.
        :param marker: The pagination query marker.
        """
        kwargs = utils.queryToKwargs(q)
        #TODO(), support pagination query
        results = [Student.from_db_model(student)
                   for student in pecan.request.storage.getStudents(**kwargs)]
        return results

    @wsmeext.pecan.wsexpose(Student, body=Student, status_code=201)
    def post(self, data):
        # TODO(), insert it into table of some database
        # and return it
        import pdb;pdb.set_trace()
        conn = pecan.request.storage
        try:
            stud = conn.createStudent(data)
            # NOTE, it needs to return the result as type of Stuent
            # so it does steps as below:
            # 1 from myproject.db.models.Student -> to a dict
            # 2 a dict of step 1 -> to myproject.api.controllers.v1.students.Student
            # myproject.db.models.Student should implement the as_dict method to get dict
            result = Student.from_db_model(stud)
        except Exception as ex:
            info = "post of StudentsController exception: %s, message: %s" % (
                ex.__class__.__name__, ex
            )
            LOG.error(info)
        return result