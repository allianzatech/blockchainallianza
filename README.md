## Allianza Blockchain – Quantum-Safe, Bridge-Free Interoperability

Allianza Blockchain is a **production-grade, testnet-first interoperability platform** that shows real cross-chain transfers like **Polygon → Bitcoin testnet** using:

- **Bridge-free design** (no custodian, no lock-and-mint bridge)
- **UChainID** for on-chain traceability of each cross-chain transfer
- **Zero-knowledge proofs (ZK proofs)** to attest state transitions
- **Quantum-safe / post-quantum security layers**

This repository contains the full backend, testnet dashboards and proof infrastructure that power  
`https://testnet.allianza.tech`.

---

### 🔥 Live Demo & Example Transaction

- **Live testnet demo**: `https://testnet.allianza.tech`  
- **Real Polygon → Bitcoin testnet transfer (latest example)**:  
  `https://live.blockcypher.com/btc-testnet/tx/2b010250667459e2bc30fd4a33f9caab937310156839c87364a5ba075594e554/`

The demo allows anyone to:

- Create a **real cross-chain transfer** (Polygon → Bitcoin testnet) with ZK proof and UChainID
- Inspect the **on-chain transaction** on a public explorer
- Verify the **ZK proof** via the embedded ZK Proof Verifier

---

### 🖼 Screenshots

> (Optional but recommended) Add PNG/GIFs to `static/` and link here.

- **Interoperability dashboard** – cross-chain transfer form, status, and proof bundle
- **ZK Proof Verifier** – quick-load by UChainID and verify proof/verification key/state hash

---

### ⚙️ Quick Start (Local)

#### 1. Requirements

- Python 3.10+
- `pip` and `virtualenv` (recommended)
- Node.js (only if you want to rebuild the Tailwind/JS assets)

#### 2. Clone & install

```bash
git clone https://github.com/allianzatech/blockchainallianza.git
cd blockchainallianza

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Environment

Create a `.env` file in the project root (or configure env vars in your platform) with, at minimum:

```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=change-me
BLOCKCYPHER_API_TOKEN=your_testnet_token_here
BITCOIN_PRIVATE_KEY=your_testnet_wif_here
```

> **Important:** never commit real mainnet keys. Only use **testnet** keys here.

#### 4. Run locally

For local development, you can start the WSGI app directly:

```bash
python allianza_blockchain.py
```

or via Gunicorn (similar to production):

```bash
gunicorn -w 2 -b 0.0.0.0:5000 --timeout 300 --keep-alive 5 --preload wsgi_optimized:application
```

Then open: `http://localhost:5000/interoperability`

---

### 🔗 Real Cross-Chain Transfers (Examples)

Some example **Bitcoin testnet** transactions produced by this system (Polygon → Bitcoin path):

- `2b010250667459e2bc30fd4a33f9caab937310156839c87364a5ba075594e554`
- _(add new hashes here as you generate more real proofs/transfers)_

Each transfer maps to a **UChainID** and **ZK proof** that can be loaded and verified in the UI.

---

### 🧠 Key Features

- **Bridge-free interoperability** – no custodial bridge, no wrapped tokens.
- **ZK proofs** – every cross-chain state transition is backed by a zero-knowledge proof.
- **UChainID** – global identifier that binds off-chain proofs and on-chain state.
- **Quantum-safe layers** – experiments with post-quantum cryptography and hardening.
- **Extensive test suite** – multiple POCs and stress tests covering interoperability and PQC.

---

### 🤝 Contributing

We welcome issues, PRs and feedback.

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-improvement`
3. Commit your changes: `git commit -m "Add my improvement"`
4. Push and open a Pull Request

See `CONTRIBUTING.md` (to be expanded) for more details and coding guidelines.

---

### 📄 License

This project is licensed under the **MIT License** – see `LICENSE` for details.


