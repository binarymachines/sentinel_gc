#!/usr/bin/env python


class TestServiceObject(object):
    def __init__(self, **kwargs):
        pass


class GoogleCloudConfigService(object):
    def __init__(self, **kwargs):
        self.config = {}
        for key, value in kwargs.items():
            self.config[key] = value


