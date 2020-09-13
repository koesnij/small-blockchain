import copy
from hashlib import sha256
import json
from time import time
from urllib.parse import urlparse

class Blockchain:
    DEFAULT_VERSION = '1.0'

    def __init__(self):
        """
        Initializes Chain, Nodes, Current Transactions
        """
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create Genesis Block
        self.new_block(100, '1')

    def register_node(self, address):
        """
        Registers new full node

        :param address: Hosts's address
        :return: None
        """
        self.nodes.add(urlparse(address).netloc)

    def new_block(self, nonce, previous_hash):
        """
        블록 생성 메소드

        :param nonce: 블록의 Nonce
        :param previous_hash: 이전 블록의 Hash
        :return: 생성된 블록
        """
        new_block = {
            'index': len(self.chain) + 1,
            'version': self.DEFAULT_VERSION,
            'previous_hash': previous_hash or self.hash_block(self.chain[-1]),
            'transactions': copy.deepcopy(self.current_transactions),
            'timestamp': time(),    #
            'nonce': nonce
        }

        self.chain.append(new_block)    # Append block to chain
        self.current_transactions.clear()   # Clear transactions to generate new block

        return new_block

    @staticmethod
    def hash_block(block):
        block_str = json.dumps(block, sort_keys=True).encode()

        return sha256(sha256(block_str).digest()).hexdigest()

    def new_transaction(self, sender, recipient, amount):
        """
        Adds new transaction to block

        :param sender: Sender's wallet ID of transaction
        :param recipient: Recipient's wallet ID of transaction
        :param amount: Amount of transaction
        :return: None
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        """
        Returns most recent block of chain
        :return: Most recent block
        """
        return self.chain[-1]

    def proof_of_work(self, prev_nonce):
        """
        Finds current block's nonce

        :param prev_nonce: Previous block's nonce
        :return: nonce
        """
        nonce = 0
        while self.is_valid_nonce(prev_nonce, nonce) is False:
            nonce += 1

        return nonce

    @staticmethod
    def is_valid_nonce(prev_nonce, nonce):
        """
        Checks nonce is valid

        :param prev_nonce: Previous block's nonce
        :param nonce: Current block's nonce
        :return: Whether nonce is valid
        """
        guess = '{0}{1}'.format(prev_nonce, nonce).encode()
        guess_hash = sha256(guess).hexdigest()

        return guess_hash[:4] == '0000'

