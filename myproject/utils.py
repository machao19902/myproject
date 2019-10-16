# -*- encoding: utf-8 -*-

from datetime import datetime

from oslo_log import log

LOG = log.getLogger(__name__)

def timeHelper(func):
    def wrapper(*args, **kwargs):
        try:
            start = datetime.now()
            info = "Begin task, start: %s" % (
                str(start))
            LOG.info(info)
            func(*args, **kwargs)
            end = datetime.now()
            diff = end - start
            info = "End task, end: %s, cost time: %s" % (
                str(end), str(diff))
            LOG.info(info)
        except Exception as ex:
            info = "Exception type is %s, message is %s" % (ex.__class__.__name__, ex)
            LOG.error(info)

    return wrapper