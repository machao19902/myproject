#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import String

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer(), nullable=False)
    userId = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)
    age = Column(Integer(), nullable=True)
    email = Column(String(256), nullable=True)
    __table_args__ = (
        Index('ix_student_userId', 'userId'),
        PrimaryKeyConstraint('id')
    )

    TRANSFORMED_FIELDS = ['id', 'userId', 'name', 'age', 'email']
    # from database model to dict
    def as_dict(self):
        result = dict()
        for field in Student.TRANSFORMED_FIELDS:
            result[field] = getattr(self, field, '')
        return result

