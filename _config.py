# coding: utf-8

"""コンフィグファイルのあれこれ


"""

from collections import namedtuple
import json
import os


def parse(path):
    return json.load(
        open(os.path.abspath(path)),
        object_hook=lambda d: namedtuple("Config", d.keys())(*d.values()))

