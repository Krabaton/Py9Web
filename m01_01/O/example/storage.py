import json
import yaml


class Storage:
    def get_value(self, key):
        raise NotImplementedError


class JSONStorage(Storage):
    def __init__(self, filename):
        self.filename = filename

    def get_value(self, key):
        with open(self.filename, 'r') as fd:
            data = json.load(fd)
            return data.get(key, None)


class YamlStorage(Storage):
    def __init__(self, filename):
        self.filename = filename

    def get_value(self, key):
        with open(self.filename, 'r') as fd:
            data = yaml.load(fd, Loader=yaml.FullLoader)
            return data.get(key, None)
