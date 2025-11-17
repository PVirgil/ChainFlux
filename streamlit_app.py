# streamlit_chainflux.py — ChainFlux narrative blockchain deployed on Streamlit

import streamlit as st
import hashlib
import json
import time
import os
from uuid import uuid4

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

# Initialize blockchain
chain = ChainFlux()

# Streamlit UI
st.set_page_config(page_title="ChainFlux", layout="centered")
st.title("🧠 ChainFlux – Narrative Blockchain")

menu = ["View Chain", "Add Event", "Mine"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "View Chain":
    for block in reversed(chain.chain):
        with st.expander(f"Block #{block.index}: {block.title}"):
            st.write("**Time:**", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp)))
            st.write("**Narrative:**", block.narrative)
            st.write("**Linked To:**", block.linked_blocks)
            st.write("**Hash:**", block.hash)
            st.write("**Previous Hash:**", block.previous_hash)

elif choice == "Add Event":
    st.subheader("Add a New Narrative Event")
    title = st.text_input("Title")
    narrative = st.text_area("Narrative")
    linked_raw = st.text_input("Linked Block Indices (comma-separated)")
    if st.button("Queue Event"):
        try:
            linked_blocks = [int(x.strip()) for x in linked_raw.split(',') if x.strip().isdigit()]
            chain.add_event(title, narrative, linked_blocks)
            st.success("Event added to the queue.")
        except:
            st.error("Invalid linked block input.")

elif choice == "Mine":
    st.subheader("Mine a Block")
    if st.button("Mine Next Event"):
        result = chain.mine()
        if result is not False:
            st.success(f"Block #{result} mined and added to chain!")
        else:
            st.warning("No unconfirmed events to mine.")
