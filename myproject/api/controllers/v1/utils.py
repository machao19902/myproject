#!/usr/bin/env python
# -*- coding: utf-8 -*-

def queryToKwargs(queryList):
    # TODO(), make it robust
    result = dict()
    if not queryList or not isinstance(queryList, list):
        return result
    for query in queryList:
        if query.op == 'eq':
            result[query.field] = result[query.value]
    return result