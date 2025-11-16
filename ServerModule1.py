import hashlib
import json
import time
import os
from uuid import uuid4
import anvil.server

CHAIN_FILE = 'chainflux.json'

class Block:
    def __init__(self, index, timestamp, title, narrative, linked_blocks, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.title = title
        self.narrative = narrative
        self.linked_blocks = linked_blocks
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'title': self.title,
            'narrative': self.narrative,
            'linked_blocks': self.linked_blocks,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class ChainFlux:
    difficulty = 2

    def __init__(self):
        self.unconfirmed_events = []
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return [Block(0, time.time(), "Genesis", "The beginning of ChainFlux.", [], "0")]

    def last_block(self):
        return self.chain[-1]

    def add_event(self, title, narrative, linked_blocks):
        self.unconfirmed_events.append({
            'title': title,
            'narrative': narrative,
            'linked_blocks': linked_blocks
        })

    def proof_of_work(self, block):
        block.nonce = 0
        hash_attempt = block.compute_hash()
        while not hash_attempt.startswith('0' * ChainFlux.difficulty):
            block.nonce += 1
            hash_attempt = block.compute_hash()
        return hash_attempt

    def add_block(self, block, proof):
        if self.last_block().hash != block.previous_hash:
            return False
        if not proof.startswith('0' * ChainFlux.difficulty):
            return False
        if proof != block.compute_hash():
            return False
        self.chain.append(block)
        self.save_chain()
        return True

    def mine(self):
        if not self.unconfirmed_events:
            return False
        data = self.unconfirmed_events.pop(0)
        last = self.last_block()
        new_block = Block(len(self.chain), time.time(), data['title'], data['narrative'], data['linked_blocks'], last.hash)
        proof = self.proof_of_work(new_block)
        if self.add_block(new_block, proof):
            return new_block.index
        return False

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump([block.__dict__ for block in self.chain], f, indent=4)

    def load_chain(self):
        if not os.path.exists(CHAIN_FILE):
            return self.create_genesis_block()
        with open(CHAIN_FILE, 'r') as f:
            data = json.load(f)
        return [Block(**b) for b in data]

chain = ChainFlux()

@anvil.server.callable
def get_chain():
    return [block.__dict__ for block in chain.chain]

@anvil.server.callable
def add_event(title, narrative, linked_blocks):
    chain.add_event(title, narrative, linked_blocks)
    return {"status": "event_added"}

@anvil.server.callable
def mine_block():
    result = chain.mine()
    if result is not False:
        return {"status": "block_mined", "block_index": result}
    return {"status": "no_events"}

