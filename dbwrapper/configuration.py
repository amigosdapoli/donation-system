#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
from configparser import ConfigParser


class Configuration(object):
    def __init__(self, config_file=os.getenv("CONFIG_PATH") ):
        if config_file is None:
            self.config_file = "dbwrapper/configs.cfg"
        else:
            self.config_file = config_file

        logging.info("Reading the config from " + self.config_file)
        self.conf = ConfigParser()
        self.conf.read(self.config_file)

    def get(self, section, key, **kwargs):
        return self.conf.get(section, key, **kwargs)

    def getboolean(self, section, key):
        return self.conf.getboolean(section, key)

    def getfloat(self, section, key):
        return self.conf.getfloat(section, key)

    def getint(self, section, key):
        return self.conf.getint(section, key)

    def has_option(self, section, key):
        return self.conf.has_option(section, key)

    def remove_option(self, section, option):
        return self.conf.remove_option(section, option)
