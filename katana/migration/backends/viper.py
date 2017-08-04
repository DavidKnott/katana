import json
import rlp
import logging
import os
from ethereum.abi import ContractTranslator
from ethereum.transactions import Transaction
from ethereum.utils import privtoaddr
from viper import compiler


# create logger
logger = logging.getLogger('MIGRATION')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Viper(object):

    # TODO ADD in options for real world deployment
    # def __init__(self, web3, contract_dir, optimize, account=None, private_key_path=None):
    def __init__(self, file, web3, contract_dir, abi_dir):
        self.file = file
        self.web3 = web3
        self.compiler = compiler
        # self.gas_price = gas_price
        self.contract_dir = contract_dir
        # self.optimize = optimize
        self._from = None
        self.private_key = None
        # if account:
        #     self._from = account
        # elif private_key_path:
        #     with open(private_key_path, 'r') as private_key_file:
        #         self.private_key = private_key_file.read().strip()
        #     self._from = self.add_0x(privtoaddr(self.private_key.hex()).encode())
        # else:
        accounts = self.web3.eth.accounts
        if len(accounts) == 0:
                raise ValueError('No account unlocked')
        self._from = accounts[0]
        # references dict maps labels to addresses
        self.references = {}
        # abis dict maps addresses to abis
        self.abis = {}
        self.total_gas = 0
        logger.info('Instructions are sent from address: {}'.format(self._from))
        balance = self.web3.eth.getBalance(self._from)
        logger.info('Address balance: {} Ether / {} Wei'.format(balance/10.0**18, balance))

    def log_transaction_receipt(self, transaction_receipt):
        gas_used = transaction_receipt['gasUsed']
        self.total_gas += gas_used
        logger.info('Transaction receipt: {} block number, {} gas used, {} cumulative gas used'.format(
            transaction_receipt['blockNumber'],
            gas_used,
            transaction_receipt['cumulativeGasUsed']
        ))

    def replace_references(self, a):
        if isinstance(a, list):
            return [self.replace_references(i) for i in a]
        else:
            return self.references[a] if isinstance(a, str) and a in self.references else a

    def compile(self, file_path):
        code = open(file_path).read()
        bytecode = self.compiler.compile(code)
        abi = self.compiler.mk_full_signature(code)
        return bytecode, abi

    def deploy(self, file_path, bytecode, abi, params, label):
        if params:
            translator = ContractTranslator(abi)
            params = [self.replace_references(p) for p in params]
            bytecode += translatore.encode_constructor_arguments(params).hex()
        # deploy contract
        logger.info('Deployment transaction for {} sent'.format(label if label else 'unknown'))
        tx_response = None
        tx = {'from':self._from, 
                  'data': bytecode, 
                #   'gas':self.gas,
                #   'gas_price':self.gas_price
                }
        # TODO implement and test private key functionality for real world deployment
        while tx_response is None or 'error' in tx_response:
                if tx_response and 'error' in tx_response:
                    logger.info('Deploy failed with error {}'.format(tx_response['error']['message']))
                    time.sleep(5)
                tx_response = self.web3.eth.sendTransaction(tx)
        transaction_receipt = self.web3.eth.getTransactionReceipt(tx_response)
        contract_address = transaction_receipt['contractAddress']
        self.references[label] = contract_address
        self.abis[contract_address] = abi
        logger.info('Contract {} created at address {}'.format(label if label else 'unknown',
                                                            contract_address))
        self.log_transaction_receipt(transaction_receipt)
    
    # Only works for testrpc
    def process(self):
        # if self.file:
            
        #     abi = self.create_abi(self.file)
        #     if abi: 
        #         self.save_abi(self.file, abi)
        # else:
        for root, directors, files in os.walk(self.contract_dir):
                for file_name in files:
                    if self.file_has_viper_ending(file_name):
                        file_path = os.path.join(root, file_name)
                        bytecode, abi = self.compile(file_path)
                        # None represents params
                        self.deploy(None,bytecode, abi, None, file_name)


    def file_has_viper_ending(self, file_name):
        return file_name.endswith('.vy') or file_name[-5:] == '.v.py'

