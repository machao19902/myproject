# -*- encoding: utf-8 -*-

from myproject import rpc

class FibonacciRPC(rpc.BaseRPC):

    def process(self):
        pass

    def fibonacci(self, context, num):
        if num <= 0:
            return -1
        if num <= 2:
            return 1
        a = 1
        b = 1
        for i in range(3, num + 1):
            a = a + b
            b = a
        return a

