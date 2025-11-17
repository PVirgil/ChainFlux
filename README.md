# 🧠 ChainFlux 

**ChainFlux** is an innovative blockchain implementation designed for storytelling, thought tracking, and causal journaling. Unlike traditional cryptocurrencies or NFT chains, ChainFlux records narrative "events" as blocks, allowing users to build a verifiable, linked history of ideas or stories.

Deployed with **Streamlit**, it provides a user-friendly interface for viewing, adding, and mining narrative blocks — making it ideal for collaborative writing, educational use, or personal knowledge networks.

---

## 🚀 Live Demo (Optional)
> https://chainflux.streamlit.app 

---

## 📦 Features

- 📖 **Narrative Blocks**: Each block includes a title, timestamp, narrative body, and references to earlier blocks
- 🔗 **Linked Inspiration**: Blocks can link to multiple previous blocks, forming non-linear story branches
- ⛏️ **Proof-of-Work Mining**: Each block must be mined with a valid hash, preserving integrity
- 💾 **Persistent Chain Storage**: Chain is stored locally in `chainflux.json`
- 🧠 **Streamlit UI**: Simple web interface for viewing the chain, adding new stories, and mining blocks

---

## 🛠️ Technologies Used

- Python 3.x
- [Streamlit](https://streamlit.io/)
- Built-in JSON for persistence
- Hashing via `hashlib`

---

## 🗂️ Project Structure

```
chainflux/
│
├── streamlit_chainflux.py     # Main app file (Streamlit UI + blockchain logic)
├── chainflux.json             # Persistent blockchain data (auto-generated)
├── requirements.txt           # Python dependencies
└── README.md                  # Project description
```

---

## 🧪 How to Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/chainflux
   cd chainflux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the app:
   ```bash
   streamlit run streamlit_chainflux.py
   ```

---

## 🔄 API-Free Architecture

This project does not expose REST endpoints. All interaction is through the Streamlit UI for clarity, simplicity, and minimal deployment overhead.

---

## 🧠 Use Cases

- Collaborative storytelling with version history
- Personal knowledge blockchain or thought graph
- Historical or fictional timelines with linked context
- Blockchain educational sandbox without coins or tokens

---

## 📈 Future Ideas

- Add export/import of chain
- Visual graph view of linked blocks
- User login or signature tracking
- Optional timestamping via external oracle

---

Crafted with care to explore how blockchain can capture not just transactions, but **thoughts, stories, and chains of inspiration**.
