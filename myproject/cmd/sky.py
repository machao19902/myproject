# -*- encoding: utf-8 -*-

import cotyledon

from myproject import service
from myproject import sky

def main():
    conf = service.prepareService()
    sm = cotyledon.ServiceManager()
    sm.add(sky.SkyService, workers=conf.sky.workers, args=(conf,))
    sm.run()