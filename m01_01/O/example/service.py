from storage import YamlStorage, JSONStorage, Storage


class Service:
    def __init__(self, storage: Storage):
        self.storage = storage

    def get(self, key):
        return self.storage.get_value(key)


if __name__ == '__main__':
    storage_json = Service(JSONStorage('data.json'))
    print(storage_json.get("name"), storage_json.get("age"))

    storage_yaml = Service(YamlStorage('data.yaml'))
    print(storage_yaml.get("name"), storage_yaml.get("age"))
