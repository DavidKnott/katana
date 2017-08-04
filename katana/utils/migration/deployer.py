import logging
from ethereum.abi import ContractTranslator
from web3 import Web3, KeepAliveRPCProvider, IPCProvider
from katana.configuration import Config



# create logger
logger = logging.getLogger('MIGRATION')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Deployer(object):
    def __init__(self, artifact, params=None):
        self.artifact = artifact.artifact
        self.params = params
        self.config = Config()
        self.references = {}
        self.web3 = Web3(KeepAliveRPCProvider(host=self.config.host, port=self.config.port))
        # TODO implement private key functionality
        self._from = self.web3.eth.accounts[0]
        self.deploy(self._from, bytes.fromhex(self.artifact['bytecode']), self.artifact['contract_name'])

    def replace_references(self, a):
        if isinstance(a, list):
            return [self.replace_references(i) for i in a]
        else:
            return self.references[a] if isinstance(a, str) and a in self.references else a

    def deploy(self, _from, bytecode, label):
        if self.params:
            translator = ContractTranslator(self.artifact['abi'])
            params = [self.replace_references(p) for p in self.params]
            bytecode += translator.encode_constructor_arguments(params)
        logger.info('Deployment transaction for {} sent'.format(label if label else 'unknown'))
        tx_response = None
        tx = {'from': _from,
                'data': bytecode}
        while tx_response is None or 'error' in tx_response:
                if tx_response and 'error' in tx_response:
                    logger.info('Deploy failed with error {}'.format(tx_response['error']['message']))
                    time.sleep(5)
                tx_response = self.web3.eth.sendTransaction(tx)
        transaction_receipt = self.web3.eth.getTransactionReceipt(tx_response)
        self.contract_address = transaction_receipt['contractAddress']
        self.references[label] = self.contract_address
        logger.info('Contract {} created at address {}'.format(label if label else 'unknown',
                                                            self.contract_address))
