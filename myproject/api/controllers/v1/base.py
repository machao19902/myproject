#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import functools
import inspect

from oslo_utils import strutils
from oslo_utils import timeutils
import pecan
import six
import wsme
from wsme import types as wtypes

operation_kind = ('lt', 'le', 'eq', 'ne', 'ge', 'gt')
operation_kind_enum = wtypes.Enum(str, *operation_kind)


class ClientSideError(wsme.exc.ClientSideError):
    def __init__(self, error, status_code=400):
        pecan.response.translatable_error = error
        super(ClientSideError, self).__init__(error, status_code)


class Base(wtypes.DynamicBase):

    @classmethod
    def from_db_model(cls, m):
        return cls(**(m.as_dict()))

    @classmethod
    def from_db_and_links(cls, m, links):
        return cls(links=links, **(m.as_dict()))

    def as_dict(self, db_model):
        valid_keys = inspect.getargspec(db_model.__init__)[0]
        if 'self' in valid_keys:
            valid_keys.remove('self')
        return self.as_dict_from_keys(valid_keys)

    def as_dict_from_keys(self, keys):
        return dict((k, getattr(self, k))
                    for k in keys
                    if hasattr(self, k) and
                    getattr(self, k) != wsme.Unset)


class Query(Base):
    """Query filter."""

    # The data types supported by the query.
    _supported_types = ['integer', 'float', 'string', 'boolean', 'datetime']

    # Functions to convert the data field to the correct type.
    _type_converters = {'integer': int,
                        'float': float,
                        'boolean': functools.partial(
                            strutils.bool_from_string, strict=True),
                        'string': six.text_type,
                        'datetime': timeutils.parse_isotime}

    _op = None  # provide a default

    def get_op(self):
        return self._op or 'eq'

    def set_op(self, value):
        self._op = value

    field = wsme.wsattr(wtypes.text, mandatory=True)
    "The name of the field to test"

    # op = wsme.wsattr(operation_kind, default='eq')
    # this ^ doesn't seem to work.
    op = wsme.wsproperty(operation_kind_enum, get_op, set_op)
    "The comparison operator. Defaults to 'eq'."

    value = wsme.wsattr(wtypes.text, mandatory=True)
    "The value to compare against the stored data"

    type = wtypes.text
    "The data type of value to compare against the stored data"

    def __repr__(self):
        # for logging calls
        return '<Query %r %s %r %s>' % (self.field,
                                        self.op,
                                        self.value,
                                        self.type)

    @classmethod
    def sample(cls):
        return cls(field='resource_id',
                   op='eq',
                   value='bd9431c1-8d69-4ad3-803a-8d4a6b89fd36',
                   type='string'
                   )

    def as_dict(self):
        return self.as_dict_from_keys(['field', 'op', 'type', 'value'])

    def _get_value_as_type(self, forced_type=None):
        """Convert metadata value to the specified data type.

        This method is called during metadata query to help convert the
        querying metadata to the data type specified by user. If there is no
        data type given, the metadata will be parsed by ast.literal_eval to
        try to do a smart converting.

        NOTE (flwang) Using "_" as prefix to avoid an InvocationError raised
        from wsmeext/sphinxext.py. It's OK to call it outside the Query class.
        Because the "public" side of that class is actually the outside of the
        API, and the "private" side is the API implementation. The method is
        only used in the API implementation, so it's OK.

        :returns: metadata value converted with the specified data type.
        """
        type = forced_type or self.type
        try:
            converted_value = self.value
            if not type:
                try:
                    converted_value = ast.literal_eval(self.value)
                except (ValueError, SyntaxError):
                    # Unable to convert the metadata value automatically
                    # let it default to self.value
                    pass
            else:
                if type not in self._supported_types:
                    # Types must be explicitly declared so the
                    # correct type converter may be used. Subclasses
                    # of Query may define _supported_types and
                    # _type_converters to define their own types.
                    raise TypeError()
                converted_value = self._type_converters[type](self.value)
                if isinstance(converted_value, datetime.datetime):
                    converted_value = timeutils.normalize_time(converted_value)
        except ValueError:
            msg = ('Unable to convert the value %(value)s to the expected data type %(type)s.'
                   ).format(value=self.value, type=type)
            raise ClientSideError(msg)
        except TypeError:
            msg = ('The data type %(type)s is not supported. The supported '
                   'data type list is: %(supported)s').format(
                type=type, supported=self._supported_types)
            raise ClientSideError(msg)
        except Exception:
            msg = ('Unexpected exception converting %(value)s to '
                   'the expected data type %(type)s.').format(
                value=self.value, type=type)
            raise ClientSideError(msg)
        return converted_value
