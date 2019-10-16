# -*- encoding: utf-8 -*-

import argparse
from datetime import datetime
import sys

from oslo_log import log
import oslo_messaging

from myproject import service

LOG = log.getLogger(__name__)


class Producer(object):
    def __init__(self, conf=None, url=None, topics=None, driver="messagingv2"):
        self.conf = conf
        self.url = url
        self.topics = topics or self.conf.sky.topics
        self.transport = oslo_messaging.get_transport(self.conf)
        self.notifier = oslo_messaging.Notifier(
            self.transport,
            topics=self.topics,
            driver=driver
        )

    def publish(self, payloads):
        try:
            self.notifier.sample(
                {},
                'sky.message',
                {"samples": payloads}
            )
            info = "send message successed, messages: {messages}".format(
                messages=payloads
            )
            LOG.info(info)
        except Exception as ex:
            info = "send message exceptin: {exception}, message: {message}, sample: {sample}".format(
                exception=ex.__class__.__name__,
                message=ex,
                sample=payloads
            )
            LOG.error(info)


def sendMessage(url=None, topics=None, payloads=None, conf=None):
    if not payloads:
        LOG.info("there is no messages to process")
        return
    producer = Producer(conf=conf, url=url, topics=topics)
    for payload in payloads:
        producer.publish(payload)


def generatePayloads(**kwargs):
    messageNum = kwargs.get('messageNum', 1)
    messageName = kwargs.get('messageName', '')
    resourceId = kwargs.get('resourceId', '')
    volume = kwargs.get('volume')
    payloads = [{
        "name": messageName,
        "resource_id": resourceId,
        'volume': volume,
        "num": i,
        'time': datetime.utcnow()
    } for i in range(messageNum)]
    return payloads


def getArgs():
    parser = argparse.ArgumentParser(
        prog='myproject',
        description='',
        epilog=''
    )
    parser.add_argument(
        '-messageName',
        help='message name',
        type=str
    )
    parser.add_argument(
        '-volume',
        help='sample volume',
        type=float,
        default=98
    )
    parser.add_argument(
        '-resourceId',
        help='id of resource',
        type=str
    )
    parser.add_argument(
        '-messageNum',
        help='how many messages you want to send',
        type=int
    )
    args = parser.parse_args()
    return args


def getParameters(args):
    if not args:
        return {}
    messageNum = args.messageNum if args.messageNum else 1
    messageName = args.messageName
    resourceId = args.resourceId
    volume = args.volume
    params = {
        'messageNum': messageNum,
        'messageName': messageName,
        'resourceId': resourceId,
        'volume': volume
    }
    return params


def main():
    args = getArgs()
    params = getParameters(args)
    sys.argv = [sys.argv[0]]
    conf = service.prepareService()
    payloads = generatePayloads(**params)
    sendMessage(payloads=payloads, conf=conf)
