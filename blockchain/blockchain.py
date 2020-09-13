import hashlib
import json
from time import time
from urllib.parse import urlparse

class Blockchain:
    DEFAULT_VERSION = '1.0'

    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create Genesis Block
        self.new_block(100, '1')

    def register_node(self, address):
        self.nodes.add(urlparse(address).netloc)

    def new_block(self, nonce, previous_hash):
        """
        블록 생성 메소드

        :param nonce: 블록의 Nonce
        :param previous_hash: 이전 블록의 Hash
        :return: 생성된 블록
        """
        block = {
            'index': len(self.chain) + 1,
            'version': self.DEFAULT_VERSION,
            'previous_hash': previous_hash or self.hash_block(self.chain[-1]),
            'transactions': self.current_transactions,
            'timestamp': time(),    #
            'nonce': nonce
        }

        self.current_transactions = []
        self.chain.append(block)

        return block

    @staticmethod
    def hash_block(block):
        block_str = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_str).hexdigest()

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_nonce):
        """
        Proof of Work Mining

        :param last_nonce:
        :return:
        """
        nonce = 0
        while self.is_valid_nonce(last_nonce, nonce) is False:
            nonce += 1

        return nonce

    @staticmethod
    def is_valid_nonce(last_nonce, nonce):
        guess = '{0}{1}'.format(last_nonce, nonce).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == '0000'

