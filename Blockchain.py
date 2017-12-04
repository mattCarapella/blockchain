import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4
from flask import Flask

class Blockchain(object):

    def __init__(self):
        self.chain = []     # stores Blockchain
        self.current_transactions = []      # stores transactions

        # Create GENESIS Block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        # Create new block and add to chain
        :param proof: <int> # Proof given by Proof of Work Algorithm
        :param previous_hash: <str> #Hash of previous block
        :return: <dict> # New block
        """

        block = {

            'index': len(self.chain)+1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):

        # Add new transaction to list of transactions
        # Creates a new transaction to go into the next mined block
        """
        :param sender <str> Address of Sender
        :param recipient <str> Address of Receiver
        :param amount <int> Amount
        :return: <int> Index of block that will hold the transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        # After adding new transaction, index of block it will be added to is returned.
        # This will be the next block to be mined.
        return self.last_block['index']+1

    @property
    def last_block(self):

        # Returns last block in the chain
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        # Create SHA256 hash of a block
        :param block: <dict> Block
        :return: <str>
        """

        # Makes sure dictionary is order to prevent inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Find number p such that hash(pp') has 4 leading zeros.
        p is the previous proof and p' is the new proof.

        :param last_proof <int>
        :return <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates proof by checking if it contains four leading zeros.
        :param last_proof <int> Previous proof
        :param proof <int> Current proof
        :return <bool> True if correct
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    app = Flask(__name__)

