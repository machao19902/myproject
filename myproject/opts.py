#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oslo_config import cfg

def list_opts():
    return [
        ('api', [
            cfg.StrOpt('paste_config',
                       default="api-paste.ini",
                       help="Configuration file for WSGI definition of API."),
            cfg.IntOpt('port',
                       default=8043,
                       help="The port for the myproject API server. (port value).")]),
        ('polling', [
            cfg.IntOpt('workers',
                       default=1,
                       required=True,
                       help="how many polling workers"),
            cfg.IntOpt('polling_interval',
                       default=10,
                       required=True,
                       help='how many seconds to poll')]),
        ('sky', [
            cfg.StrOpt('exchange',
                       default='myproject',
                       help='exchange name'),
            cfg.ListOpt('topics',
                        default=['sky'],
                        help='topic list'),
            cfg.IntOpt('workers',
                       default=1,
                       help='number of worker')])
    ]

