# -*- encoding: utf-8 -*-

import abc
from datetime import datetime
import sys
import threading
import time

import cotyledon
from cotyledon import oslo_config_glue
from oslo_config import cfg
from oslo_log import log
from oslo_utils import timeutils
import six

from myproject import service

LOG = log.getLogger(__name__)

OPTS = [
    cfg.IntOpt('workers',
               default=1,
               required=True,
               help="how many polling workers"),
    cfg.IntOpt('polling_interval',
               default=10,
               required=True,
               help='how many seconds to poll')
]


@six.add_metaclass(abc.ABCMeta)
class BaseTask(cotyledon.Service):

    def __init__(self, workerId, conf, interval=0):
        super(BaseTask, self).__init__(workerId)
        self.workerId = workerId
        self.interval = interval
        self.closeEvent = threading.Event()
        self.conf = conf

    # main entry point
    def run(self):
        time.sleep(self.workerId)
        while not self.closeEvent.is_set():
            with timeutils.StopWatch() as timer:
                self.process()
                elapsedTime = self.interval - timer.elapsed(0)
                timeout = max(0, elapsedTime)
                self.closeEvent.wait(timeout)
        self.closeEvent.set()

    @abc.abstractmethod
    def process(self):
        """ Process code """

    def terminate(self):
        self.closeEvent.set()
        self.closeService()

    @staticmethod
    def closeService():
        pass


class PollingTask(BaseTask):
    def __init__(self, workerId, conf):
        interval = conf.polling.polling_interval
        super(PollingTask, self).__init__(workerId, conf, interval=interval)

    # TODO(), add process code
    def process(self):
        info = "process at {curTime}".format(
            curTime=datetime.now()
        )
        print info
        LOG.info(info)


class PollingServiceManager(cotyledon.ServiceManager):

    def __init__(self, conf):
        super(PollingServiceManager, self).__init__()
        oslo_config_glue.setup(self, conf)
        self.conf = conf
        self.addService()

    # add service which needs to be managered
    def addService(self):
        # NOTE(), args=(self.conf,) it needs to add ','
        self.pollingProcessId = self.add(
            PollingTask,
            args=(self.conf,),
            workers=self.conf.polling.workers)

    def on_reload(self):
        self.reconfigure(
            self.pollingProcessId,
            workers=self.conf.polling.workers
        )

    def run(self):
        super(PollingServiceManager, self).run()


def pollingd():
    # initialize config
    conf = service.prepareService()
    PollingServiceManager(conf).run()
