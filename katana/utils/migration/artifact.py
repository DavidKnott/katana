from katana.compilation import get_compiler
from katana.configuration import Config

#TODO add in support of other languages, (add contract name)
class Artifact(object):
    def __init__(self, file_path):
        self.config = Config()
        self.compiler = get_compiler(self.config.language)
        self.artifact = self.compiler(None, None, None).compile(file_path)
