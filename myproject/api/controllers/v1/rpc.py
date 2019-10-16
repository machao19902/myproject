# -*- encoding: utf-8 -*-

from oslo_config import cfg
import pecan
from pecan import rest
import wsme
from wsme import types as wtypes
import wsmeext.pecan

from myproject.api.controllers.v1 import base
from myproject import messaging

class Fibonacci(base.Base):
    def as_dict(self):
        return self.as_dict_from_keys(['num', 'host'])

    num = int
    host = wtypes.text


class RpcController(rest.RestController):

    _custom_actions = {
        'fibonacci': ['POST'],
    }

    def __init__(self):
        self.rpcClient = messaging.get_rpc_client(
            messaging.get_transport(),
            version='1.0'
        )

    ''' test url
    
    curl -X POST http://127.0.0.1:8043/v1/rpc/fibonacci 
    -H "Content-Type: application/json" -d '{"num": 3, "host": "localhost.localdomain"}' -v
    '''
    @wsmeext.pecan.wsexpose(int, body=Fibonacci, status_code=201)
    def fibonacci(self, data):
        num = data.num
        host = data.host
        method = 'fibonacci'
        topic = '{rpcTopic}.{host}'.format(
            rpcTopic=pecan.request.cfg.rpc.topic,
            host=host
        )
        cxt = {}
        kwargs = {
            'num': num
        }
        result = self.rpcClient.prepare(topic=topic).call(cxt, method, **kwargs)
        return result
