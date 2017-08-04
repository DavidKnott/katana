import os
import logging
import json
from viper import compiler 
from subprocess import CalledProcessError

# create logger
logger = logging.getLogger('ABI')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Viper(object):

    def __init__(self, file, contract_dir, abi_dir):
        self.file = file
        self.contract_dir = contract_dir
        self.abi_dir = abi_dir
        self.compiler = compiler

    @staticmethod
    def get_file_name(file_path):
        return file_path.split("/")[-1].split(".")[0]

    def compile(self, file_path):
        file_name = file_path.split("/")[-1]
        code = open(file_path).read()
        bytecode = self.compiler.compile(code).hex()
        abi = self.compiler.mk_full_signature(code)
        return {"contract_name":file_name,
                "bytecode": bytecode,
                "abi":abi}

    def save_artifact(self, artifact):
        file_name = artifact["contract_name"]
        import pdb; pdb.set_trace()
        if not os.path.exists(self.abi_dir):
            os.mkdir(self.abi_dir)
        # if not os.path.exits(file_path):
        with open('{}/{}.json'.format(self.abi_dir, file_name), 'w+') as artifact_file:
            artifact_file.write(json.dumps(artifact, indent=4, separators=(',', ': ')))
            artifact_file.close()
        logger.info('{} artifact generated.'.format(file_name))
    
# TODO add specific file functionality
    def process(self):
        for root, directors, files in os.walk(self.contract_dir):
            for file_name in files:
                if self.file_has_viper_ending(file_name):
                    file_path = os.path.join(root, file_name)
                    artifact = self.compile(file_path)
                    if artifact:
                        self.save_artifact(artifact)

    def file_has_viper_ending(self, file_name):
        return file_name.endswith('.vy') or file_name[-5:] == '.v.py'
