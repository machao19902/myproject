#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
from datetime import datetime

import cotyledon
from oslo_log import log
import oslo_messaging
import six

from myproject import messaging

LOG = log.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class BaseNotificationEndpoint(object):

    @abc.abstractmethod
    def sample(self, notifications):
        """"""


class SkyEndpoint(BaseNotificationEndpoint):

    def __init__(self):
        pass

    def sample(self, notifications):
        # TODO(), add real process notification code
        info = "process ends at: {curTime}, notifications: {notifications}".format(
            notifications=notifications,
            curTime=datetime.now()
        )
        LOG.info(info)

class SkyService(cotyledon.Service):

    def __init__(self, worker_id, conf):
        LOG.info('start {service}'.format(service=self.__class__.__name__))
        super(SkyService, self).__init__(worker_id)
        self.conf = conf
        self.transport = None
        self.targets = None
        self.endpoints = None
        self.listener = None
        self.rpc_server = None

    def getTransport(self):
        if not self.transport:
            try:
                self.transport = messaging.get_transport()
            except Exception as ex:
                info = "get transport exception: {exception}, " \
                       "message: {message}".format(exception=ex.__class__.__name__,
                                                   message=ex)
                LOG.error(info)
        return self.transport

    def getEndpoints(self):
        if not self.endpoints:
            try:
                # TODO(), use entry_points to get real endpoints
                self.endpoints = [SkyEndpoint()]
            except Exception as ex:
                info = "get endpoints exception: {exception}, " \
                       "message: {message}".format(exception=ex.__class__.__name__,
                                                   message=ex)
                LOG.error(info)
        return self.endpoints

    def getTargets(self):
        if not self.targets:
            try:
                topics = self.conf.sky.topics
                exchange = self.conf.sky.exchange
                targets = []
                for topic in topics:
                    target = oslo_messaging.Target(
                        topic=topic,
                        exchange=exchange
                    )
                    targets.append(target)
                self.targets = targets
            except Exception as ex:
                info = "get targets exception: {exception}, " \
                       "message: {message}".format(exception=ex.__class__.__name__,
                                                   message=ex)
                LOG.error(info)
        return self.targets

    '''
    initialize message listener:
    1 initialize transport with url or oslo.Config object
    2 initialize endpoints which is the real object lists to consume message,
    if oslo_messaging.Notifier.sample is called, then the endpoint must have
    sample(notification) method
    3 initialize targets which means you want to listen which messaged you
    are intersted in, each target can include topic and exchange.
    4 then you can get message listener with parameters allow_requeue, batch_size
    and so on
    '''
    def startListener(self):
        transport = self.getTransport()
        endpoints = self.getEndpoints()
        targets = self.getTargets()
        self.listener = messaging.get_batch_notification_listener(
            transport,
            targets,
            endpoints,
            allow_requeue=True,
            batch_size=1,
            batch_timeout=None
        )
        self.listener.start(override_pool_size=1)

    def run(self):
        try:
            self.startListener()
            LOG.info("start listener finished")
        except Exception as ex:
            info = "run exception: {exception}, " \
                   "message: {message}".format(exception=ex.__class__.__name__,
                                               message=ex)
            LOG.error(info)
