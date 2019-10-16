# -*- encoding: utf-8 -*-

import abc

import six
from stevedore import driver
from stevedore import extension

@six.add_metaclass(abc.ABCMeta)
class BaseRPC(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def process(self):
        """ RPC process method """


def loadRpcManagers(namespace='myproject.rpc'):
    return extension.ExtensionManager(
        namespace=namespace,
        invoke_on_load=True
    )


def getRpcManager(name, namespace='myproject.rpc'):
    manager = driver.DriverManager(
        namespace=namespace,
        name=name,
        invoke_on_load=True,
        invoke_args=(),
    )
    return manager.driver
