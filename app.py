# ChainFlux – Narrative Blockchain of Inspired Events
# Each block holds a title, narrative, and linked moments (references to prior blocks)

import hashlib
import json
import time
import os
from flask import Flask, jsonify, request, render_template_string

CHAIN_FILE = 'chainflux.json'

class Block:
    def __init__(self, index, timestamp, title, narrative, linked_blocks, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.title = title
        self.narrative = narrative
        self.linked_blocks = linked_blocks  # list of block indices
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

        last = self.last_block()
        data = self.unconfirmed_events.pop(0)
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            title=data['title'],
            narrative=data['narrative'],
            linked_blocks=data['linked_blocks'],
            previous_hash=last.hash
        )

        proof = self.proof_of_work(new_block)
        return self.add_block(new_block, proof)

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump([block.__dict__ for block in self.chain], f, indent=4)

    def load_chain(self):
        if not os.path.exists(CHAIN_FILE):
            return self.create_genesis_block()
        with open(CHAIN_FILE, 'r') as f:
            data = json.load(f)
        return [Block(**b) for b in data]

# ----------------- Flask App -----------------

app = Flask(__name__)
chain = ChainFlux()

@app.route('/')
def home():
    html = """
    <html><head><title>ChainFlux Explorer</title><style>
    body { font-family: sans-serif; background: #f9f9f9; padding: 20px; }
    .block { background: white; padding: 20px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 0 6px rgba(0,0,0,0.05); }
    h2 { margin: 0; }
    </style></head><body>
    <h1>🧠 ChainFlux: Narrative Blockchain</h1>
    {% for block in chain %}
    <div class="block">
        <h2>#{{ block.index }}: {{ block.title }}</h2>
        <p><b>Time:</b> {{ block.timestamp }}</p>
        <p><b>Links to:</b> {{ block.linked_blocks }}</p>
        <p><b>Hash:</b> {{ block.hash }}</p>
        <p><b>Prev:</b> {{ block.previous_hash }}</p>
        <p>{{ block.narrative }}</p>
    </div>
    {% endfor %}
    </body></html>
    """
    return render_template_string(html, chain=[block.__dict__ for block in chain.chain])

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    required = ['title', 'narrative', 'linked_blocks']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing fields'}), 400
    chain.add_event(data['title'], data['narrative'], data['linked_blocks'])
    return jsonify({'message': 'Event added to queue'})

@app.route('/mine')
def mine():
    success = chain.mine()
    return jsonify({'message': 'Block added' if success else 'No events to mine'})

@app.route('/chain')
def full_chain():
    return jsonify([block.__dict__ for block in chain.chain])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
