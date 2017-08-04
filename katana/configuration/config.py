import json

class Config(object):
    def __init__(self):
        self.json_config = self.read_katana_config_json()
        self.host = self.json_config["networks"]["development"]["host"]
        self.port = self.json_config["networks"]["development"]["port"]
        self.language= self.json_config["language"]

    def read_katana_config_json(self):
        try:
            raw_config = open("./katana.json").read()
        except FileNotFoundError as e:
            raise type(e)(e.messsage + ("please create a katana.json file"))
        return json.loads(raw_config)