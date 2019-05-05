#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from alembic import command
from alembic import config
from alembic import migration
from oslo_db.sqlalchemy import session as dbSession

from myproject.db import base
from myproject.db import models


class Connection(base.Connection):
    def __init__(self, conf):
        self.conf = conf
        options = dict(conf.database)
        options['max_retries'] = 0
        self.engineFacade = dbSession.EngineFacade(
            conf.database.connection,
            **options)

    def getAlembicConfig(self):
        dirName = os.path.dirname(__file__)
        realDirName = os.path.dirname(dirName)
        path = "%s/migrate/alembic.ini" % (realDirName)
        cfg = config.Config(path)
        cfg.set_main_option(
            'sqlalchemy.url', self.conf.database.connection)
        return cfg

    def upgrade(self, noCreate=False):
        # import pdb;pdb.set_trace()
        cfg = self.getAlembicConfig()
        cfg.conf = self.conf
        if noCreate:
            command.upgrade(cfg, "head")
        else:
            engine = self.engineFacade.get_engine()
            ctxt = migration.MigrationContext.configure(engine.connect())
            currentVersion = ctxt.get_current_revision()
            if currentVersion is None:
                models.Base.metadata.create_all(engine, checkfirst=False)
                command.stamp(cfg, "head")
            else:
                command.upgrade(cfg, "head")

    @staticmethod
    def rowToStudentModel(row):
        result = models.Student(
            id=row.id,
            userId=row.userId,
            name=row.name,
            age=row.age,
            email=row.email
        )
        return result

    def retrieveStudents(self, query):
        return (self.rowToStudentModel(obj) for obj in query.all())

    def getStudents(self, id=None, userId=None, name=None,
                    age=None, email=None, pagination=None):
        # NOTE, pagination is needed
        pagination = pagination or {}
        session = self.engineFacade.get_session()
        query = session.query(models.Student)
        if id is not None:
            query = query.filter(models.Student.id == id)
        if userId is not None:
            query = query.filter(models.Student.userId == userId)
        if name is not None:
            query = query.filter(models.Student.name == name)
        if age is not None:
            query = query.filter(models.Student.age == age)
        if email is not None:
            query = query.filter(models.Student.email == email)
        # TODO(), add pagination query
        students = self.retrieveStudents(query)
        return students

    def createStudent(self, obj):
        session = self.engineFacade.get_session()
        row = models.Student(
            userId=obj.userId,
            name=obj.name,
            age=obj.age,
            email=obj.email
        )
        with session.begin():
            session.add(row)
        return row

    def updateStudent(self, obj):
        session = self.engineFacade.get_session()
        with session.begin():
            count = session.query(models.Student).filter(
                models.Student.id == obj.id).update(
                obj.as_dict()
            )
            if not count:
                raise "Not found student with id: %s" % obj.id
        return obj

    def deleteStudent(self, id):
        session = self.engineFacade.get_session()
        with session.begin():
            session.query(models.Student).filter(
                models.Student.id == id).delete()
