# DApp Template Files

This file contains the structure and code content of the Pharos DApp templates (Foundry and Hardhat).

## File List

- `foundry/.gitignore`
- `foundry/app/.keep`
- `foundry/app/App.jsx`
- `foundry/app/main.jsx`
- `foundry/contract/.env`
- `foundry/contract/.github/workflows/test.yml`
- `foundry/contract/.gitignore`
- `foundry/contract/.keep`
- `foundry/contract/README.md`
- `foundry/contract/foundry.toml`
- `foundry/contract/script/Counter.s.sol`
- `foundry/contract/src/Counter.sol`
- `foundry/contract/test/Counter.t.sol`
- `foundry/index.html`
- `foundry/package.json`
- `foundry/vite.config.js`
- `hardhat/.gitignore`
- `hardhat/app/.keep`
- `hardhat/app/app.jsx`
- `hardhat/app/main.jsx`
- `hardhat/contract/.env`
- `hardhat/contract/.gitignore`
- `hardhat/contract/README.md`
- `hardhat/contract/contracts/Counter.sol`
- `hardhat/contract/hardhat.config.js`
- `hardhat/contract/ignition/modules/Counter.js`
- `hardhat/contract/package.json`
- `hardhat/index.html`
- `hardhat/package.json`
- `hardhat/vite.config.js`

---

### File: `foundry/.gitignore`

```
# Compiler files
cache/
out/

# Ignores development broadcast logs
!/broadcast
/broadcast/*/31337/
/broadcast/**/dry-run/

# Docs
docs/

# Dotenv file
.env
package-lock.json
node_modules/

node_modules
.env

# Hardhat files
/cache
/artifacts

# TypeChain files
/typechain
/typechain-types

# solidity-coverage files
/coverage
/coverage.json

# Hardhat Ignition default folder for deployments against a local node
ignition/deployments/chain-31337

```

---

### File: `foundry/app/.keep`

```

```

---

### File: `foundry/app/App.jsx`

```javascript
import React, { useState, useEffect } from "react";
import { ethers } from "ethers";

const defaultContractAddress = "0x4477855B8e80AD1023eFd4B368320D11623F0d6f";

const abi = [
    {
        "inputs": [],
        "name": "number",
        "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{ "internalType": "uint256", "name": "newNumber", "type": "uint256" }],
        "name": "setNumber",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "increment",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
];

function App() {
    const [contractAddress, setContractAddress] = useState(defaultContractAddress);
    const [counter, setCounter] = useState("Not fetched");
    const [inputValue, setInputValue] = useState("");
    const [walletAddress, setWalletAddress] = useState("");
    const [status, setStatus] = useState("Ready");

    // Connect wallet
    const connectWallet = async () => {
        if (walletAddress) {
            setStatus(`Already connected: ${walletAddress}`);
            return;
        }
        if (!window.ethereum) {
            setStatus("Web3 provider (MetaMask) not detected. Please install it to connect.");
            return;
        }
        try {
            setStatus("Connecting wallet...");
            const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
            if (accounts && accounts.length > 0) {
                setWalletAddress(accounts[0]);
                setStatus("Wallet connected successfully!");
            } else {
                setStatus("No accounts returned from Web3 provider.");
            }
        } catch (err) {
            setStatus(`Connection error: ${err.message || err}`);
        }
    };

    // Get contract instance
    const getContract = async () => {
        if (!window.ethereum) throw new Error("MetaMask is not installed.");
        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const signer = provider.getSigner();
        return new ethers.Contract(contractAddress, abi, signer);
    };

    // Fetch the counter value
    const handleGet = async () => {
        try {
            setStatus("Fetching current counter value...");
            const contract = await getContract();
            const val = await contract.number();
            setCounter(val.toString());
            setStatus("Counter value retrieved!");
        } catch (err) {
            console.error(err);
            setStatus(`Fetch error: ${err.message || err}`);
        }
    };

    // Set counter value
    const handleSet = async () => {
        if (!inputValue) {
            setStatus("Please enter a number.");
            return;
        }
        try {
            setStatus("Sending transaction to set number...");
            const contract = await getContract();
            const tx = await contract.setNumber(inputValue);
            setStatus("Transaction pending... Please wait.");
            await tx.wait();
            setStatus("Counter successfully set on-chain!");
            setInputValue("");
            handleGet(); // Auto refresh
        } catch (err) {
            console.error(err);
            setStatus(`Transaction failed: ${err.message || err}`);
        }
    };

    // Increment counter value
    const handleIncrement = async () => {
        try {
            setStatus("Sending transaction to increment...");
            const contract = await getContract();
            const tx = await contract.increment();
            setStatus("Transaction pending... Please wait.");
            await tx.wait();
            setStatus("Counter successfully incremented!");
            handleGet(); // Auto refresh
        } catch (err) {
            console.error(err);
            setStatus(`Increment failed: ${err.message || err}`);
        }
    };

    // Listen for account updates
    useEffect(() => {
        if (window.ethereum) {
            window.ethereum.request({ method: "eth_accounts" })
                .then((accounts) => {
                    if (accounts && accounts.length > 0) setWalletAddress(accounts[0]);
                })
                .catch((err) => console.error("Error checking accounts", err));

            const handleAccounts = (accounts) => {
                setWalletAddress(accounts[0] || "");
            };

            if (window.ethereum.on) {
                window.ethereum.on("accountsChanged", handleAccounts);
            }

            return () => {
                if (window.ethereum.removeListener) {
                    window.ethereum.removeListener("accountsChanged", handleAccounts);
                }
            };
        }
    }, []);

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                {/* Header */}
                <div style={styles.header}>
                    <div>
                        <h1 style={styles.title}>Counter dApp</h1>
                        <span style={styles.subtitle}>Pharos Atlantic Testnet Quickstart</span>
                    </div>
                    <button 
                        onClick={connectWallet} 
                        style={walletAddress ? styles.walletBadge : styles.connectBtn}
                    >
                        {walletAddress 
                            ? `${walletAddress.substring(0, 6)}...${walletAddress.substring(38)}` 
                            : "Connect Wallet"}
                    </button>
                </div>

                {/* Contract Input */}
                <div style={styles.formGroup}>
                    <label style={styles.label}>Contract Address</label>
                    <input 
                        type="text" 
                        value={contractAddress}
                        onChange={(e) => setContractAddress(e.target.value)}
                        style={styles.input}
                    />
                </div>

                {/* Display Value */}
                <div style={styles.displayCard}>
                    <div style={styles.displayLabel}>On-chain Counter Value</div>
                    <div style={styles.displayValue}>{counter}</div>
                    <button onClick={handleGet} style={styles.refreshBtn}>Refresh Value</button>
                </div>

                {/* Actions */}
                <div style={styles.actions}>
                    <div style={{ display: "flex", gap: "10px" }}>
                        <input 
                            type="number" 
                            placeholder="New Value" 
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            style={{ ...styles.input, flex: 1 }}
                        />
                        <button onClick={handleSet} style={styles.primaryBtn}>Set Value</button>
                    </div>
                    
                    <button onClick={handleIncrement} style={styles.accentBtn}>
                        🚀 Increment Counter (+1)
                    </button>
                </div>

                {/* Status Bar */}
                <div style={styles.statusBar}>
                    <strong>Status:</strong> {status}
                </div>
            </div>
        </div>
    );
}

// Sleek and simple inline styles for quick development template
const styles = {
    container: {
        maxWidth: "600px",
        margin: "80px auto",
        padding: "0 20px",
        fontFamily: "'Inter', sans-serif",
    },
    card: {
        background: "rgba(30, 41, 59, 0.5)",
        backdropFilter: "blur(12px)",
        WebkitBackdropFilter: "blur(12px)",
        border: "1px solid rgba(255, 255, 255, 0.08)",
        borderRadius: "16px",
        padding: "30px",
        boxShadow: "0 20px 40px rgba(0, 0, 0, 0.4)",
    },
    header: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
        paddingBottom: "18px",
        marginBottom: "22px",
    },
    title: {
        fontFamily: "'Outfit', sans-serif",
        fontSize: "1.8rem",
        fontWeight: "800",
        background: "linear-gradient(135deg, #c084fc 0%, #6366f1 100%)",
        WebkitBackgroundClip: "text",
        WebkitTextFillColor: "transparent",
        margin: 0,
    },
    subtitle: {
        fontSize: "0.85rem",
        color: "#64748b",
    },
    connectBtn: {
        background: "linear-gradient(135deg, #6366f1, #4f46e5)",
        border: "none",
        color: "#fff",
        padding: "8px 16px",
        borderRadius: "8px",
        fontWeight: "600",
        cursor: "pointer",
        transition: "opacity 0.2s",
    },
    walletBadge: {
        background: "rgba(99, 102, 241, 0.12)",
        border: "1px solid rgba(99, 102, 241, 0.25)",
        color: "#818cf8",
        padding: "8px 16px",
        borderRadius: "8px",
        fontWeight: "600",
        fontFamily: "monospace",
        cursor: "default",
    },
    formGroup: {
        display: "flex",
        flexDirection: "column",
        gap: "6px",
        marginBottom: "20px",
    },
    label: {
        fontSize: "0.75rem",
        fontWeight: "700",
        color: "#94a3b8",
        textTransform: "uppercase",
        letterSpacing: "0.05em",
    },
    input: {
        background: "rgba(15, 23, 42, 0.6)",
        border: "1px solid rgba(255, 255, 255, 0.08)",
        borderRadius: "8px",
        padding: "10px 14px",
        color: "#f8fafc",
        fontSize: "0.9rem",
        outline: "none",
    },
    displayCard: {
        background: "rgba(15, 23, 42, 0.4)",
        border: "1px solid rgba(255, 255, 255, 0.04)",
        borderRadius: "10px",
        padding: "18px",
        textAlign: "center",
        marginBottom: "20px",
        position: "relative",
    },
    displayLabel: {
        fontSize: "0.8rem",
        color: "#94a3b8",
        marginBottom: "6px",
    },
    displayValue: {
        fontFamily: "'Outfit', sans-serif",
        fontSize: "2rem",
        fontWeight: "800",
        color: "#f8fafc",
        marginBottom: "8px",
    },
    refreshBtn: {
        background: "transparent",
        border: "1px solid rgba(255, 255, 255, 0.15)",
        color: "#94a3b8",
        padding: "4px 10px",
        borderRadius: "6px",
        fontSize: "0.75rem",
        cursor: "pointer",
        transition: "all 0.2s",
    },
    actions: {
        display: "flex",
        flexDirection: "column",
        gap: "12px",
        marginBottom: "20px",
    },
    primaryBtn: {
        background: "linear-gradient(135deg, #6366f1, #4f46e5)",
        border: "none",
        color: "#fff",
        padding: "10px 18px",
        borderRadius: "8px",
        fontWeight: "600",
        cursor: "pointer",
    },
    accentBtn: {
        background: "linear-gradient(135deg, #ec4899, #db2777)",
        border: "none",
        color: "#fff",
        padding: "12px 18px",
        borderRadius: "8px",
        fontWeight: "700",
        cursor: "pointer",
        textAlign: "center",
    },
    statusBar: {
        fontSize: "0.8rem",
        color: "#94a3b8",
        background: "rgba(15, 23, 42, 0.6)",
        padding: "8px 12px",
        borderRadius: "6px",
        border: "1px solid rgba(255, 255, 255, 0.05)",
        wordBreak: "break-all",
    }
};

export default App;
```

---

### File: `foundry/app/main.jsx`

```javascript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
)
```

---

### File: `foundry/contract/.env`

```
PHAROS_MAINNET_RPC_URL="https://pharos-mainnet.g.alchemy.com/v2/ecck2p9w9oZkTCfiXjl3w"
PHAROS_ATLANTIC_RPC_URL="https://pharos-atlantic.g.alchemy.com/v2/ecck2p9w9oZkTCfiXjl3w"
PHAROS_MAINNET_CHAIN_ID="688688"
PHAROS_ATLANTIC_CHAIN_ID="688689"
PRIVATE_KEY=4f34a2df8cc58b9fe7a8f7a807875f02068b28652b2a74df5b760685e88a5a41

```

---

### File: `foundry/contract/.github/workflows/test.yml`

```yaml
name: CI

on:
  push:
  pull_request:
  workflow_dispatch:

env:
  FOUNDRY_PROFILE: ci

jobs:
  check:
    strategy:
      fail-fast: true

    name: Foundry project
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Install Foundry
        uses: foundry-rs/foundry-toolchain@v1

      - name: Show Forge version
        run: |
          forge --version

      - name: Run Forge fmt
        run: |
          forge fmt --check
        id: fmt

      - name: Run Forge build
        run: |
          forge build --sizes
        id: build

      - name: Run Forge tests
        run: |
          forge test -vvv
        id: test

```

---

### File: `foundry/contract/.gitignore`

```
# Compiler files
cache/
out/
lib/

# Ignores development broadcast logs
!/broadcast
/broadcast/*/31337/
/broadcast/**/dry-run/

# Docs
docs/

# Dotenv file
.env

```

---

### File: `foundry/contract/.keep`

```

```

---

### File: `foundry/contract/README.md`

```markdown
## Foundry

**Foundry is a blazing fast, portable and modular toolkit for Ethereum application development written in Rust.**

Foundry consists of:

-   **Forge**: Ethereum testing framework (like Truffle, Hardhat and DappTools).
-   **Cast**: Swiss army knife for interacting with EVM smart contracts, sending transactions and getting chain data.
-   **Anvil**: Local Ethereum node, akin to Ganache, Hardhat Network.
-   **Chisel**: Fast, utilitarian, and verbose solidity REPL.

## Documentation

https://book.getfoundry.sh/

## Usage

### Build

```shell
$ forge build
```

### Test

```shell
$ forge test
```

### Format

```shell
$ forge fmt
```

### Gas Snapshots

```shell
$ forge snapshot
```

### Anvil

```shell
$ anvil
```

### Deploy

```shell
$ forge script script/Counter.s.sol:CounterScript --rpc-url <your_rpc_url> --private-key <your_private_key>
```

### Cast

```shell
$ cast <subcommand>
```

### Help

```shell
$ forge --help
$ anvil --help
$ cast --help
```

```

---

### File: `foundry/contract/foundry.toml`

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
env = ".env"

# See more config options https://github.com/foundry-rs/foundry/blob/master/crates/config/README.md#all-options

```

---

### File: `foundry/contract/script/Counter.s.sol`

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import {Counter} from "../src/Counter.sol";

contract CounterScript is Script {
    Counter public counter;

    function setUp() public {}

    function run() public {
        vm.startBroadcast();

        counter = new Counter();

        vm.stopBroadcast();
    }
}

```

---

### File: `foundry/contract/src/Counter.sol`

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Counter {
    uint256 public number;

    function setNumber(uint256 newNumber) public {
        number = newNumber;
    }

    function increment() public {
        number++;
    }

    // Compatibility functions for Simple Storage integration
    function set(uint256 newNumber) public {
        number = newNumber;
    }

    function get() public view returns (uint256) {
        return number;
    }
}

```

---

### File: `foundry/contract/test/Counter.t.sol`

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {Counter} from "../src/Counter.sol";

contract CounterTest is Test {
    Counter public counter;

    function setUp() public {
        counter = new Counter();
        counter.setNumber(0);
    }

    function test_Increment() public {
        counter.increment();
        assertEq(counter.number(), 1);
    }

    function testFuzz_SetNumber(uint256 x) public {
        counter.setNumber(x);
        assertEq(counter.number(), x);
    }
}

```

---

### File: `foundry/index.html`

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Simple Storage & Counter dApp | Pharos Atlantic</title>
    <!-- Premium Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #0b0f19;
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,0.3) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(271,76%,53%,0.15) 0, transparent 50%),
                radial-gradient(at 50% 100%, hsla(224,71%,4%,1) 0, transparent 100%);
            background-attachment: fixed;
            color: #f8fafc;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
        }
    </style>
</head>

<body>
    <div id="root"></div>
    <script type="module" src="/app/main.jsx"></script>
</body>

</html>
```

---

### File: `foundry/package.json`

```json
{
  "name": "dapp",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "ethers": "^5.7.2",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.4.1"
  }
}
```

---

### File: `foundry/vite.config.js`

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
});
```

---

### File: `hardhat/.gitignore`

```
# Compiler files
cache/
out/

# Ignores development broadcast logs
!/broadcast
/broadcast/*/31337/
/broadcast/**/dry-run/

# Docs
docs/

# Dotenv file
.env
package-lock.json
node_modules/

node_modules
.env

# Hardhat files
/cache
/artifacts

# TypeChain files
/typechain
/typechain-types

# solidity-coverage files
/coverage
/coverage.json

# Hardhat Ignition default folder for deployments against a local node
ignition/deployments/chain-31337

```

---

### File: `hardhat/app/.keep`

```

```

---

### File: `hardhat/app/app.jsx`

```javascript
import React, { useState, useEffect } from "react";
import { ethers } from "ethers";

const defaultContractAddress = "0xbc9737672921C401CbCC9Eca4eE19DaD42AA2a68"; // Replace with your contract address once deployed

const abi = [
    {
        "inputs": [],
        "name": "number",
        "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{ "internalType": "uint256", "name": "newNumber", "type": "uint256" }],
        "name": "setNumber",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "increment",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
];

function App() {
    const [contractAddress, setContractAddress] = useState(defaultContractAddress);
    const [counter, setCounter] = useState("Not fetched");
    const [inputValue, setInputValue] = useState("");
    const [walletAddress, setWalletAddress] = useState("");
    const [status, setStatus] = useState("Ready");

    // Connect wallet
    const connectWallet = async () => {
        if (walletAddress) {
            setStatus(`Already connected: ${walletAddress}`);
            return;
        }
        if (!window.ethereum) {
            setStatus("Web3 provider (MetaMask) not detected. Please install it to connect.");
            return;
        }
        try {
            setStatus("Connecting wallet...");
            const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
            if (accounts && accounts.length > 0) {
                setWalletAddress(accounts[0]);
                setStatus("Wallet connected successfully!");
            } else {
                setStatus("No accounts returned from Web3 provider.");
            }
        } catch (err) {
            setStatus(`Connection error: ${err.message || err}`);
        }
    };

    // Get contract instance
    const getContract = async () => {
        if (!window.ethereum) throw new Error("MetaMask is not installed.");
        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const signer = provider.getSigner();
        return new ethers.Contract(contractAddress, abi, signer);
    };

    // Fetch the counter value
    const handleGet = async () => {
        if (contractAddress === "YOUR_CONTRACT_ADDRESS") {
            setStatus("Please replace 'YOUR_CONTRACT_ADDRESS' with your actual deployed contract address first.");
            return;
        }
        try {
            setStatus("Fetching current counter value...");
            const contract = await getContract();
            const val = await contract.number();
            setCounter(val.toString());
            setStatus("Counter value retrieved!");
        } catch (err) {
            console.error(err);
            setStatus(`Fetch error: ${err.message || err}`);
        }
    };

    // Set counter value
    const handleSet = async () => {
        if (contractAddress === "YOUR_CONTRACT_ADDRESS") {
            setStatus("Please enter a valid deployed contract address.");
            return;
        }
        if (!inputValue) {
            setStatus("Please enter a number.");
            return;
        }
        try {
            setStatus("Sending transaction to set number...");
            const contract = await getContract();
            const tx = await contract.setNumber(inputValue);
            setStatus("Transaction pending... Please wait.");
            await tx.wait();
            setStatus("Counter successfully set on-chain!");
            setInputValue("");
            handleGet(); // Auto refresh
        } catch (err) {
            console.error(err);
            setStatus(`Transaction failed: ${err.message || err}`);
        }
    };

    // Increment counter value
    const handleIncrement = async () => {
        if (contractAddress === "YOUR_CONTRACT_ADDRESS") {
            setStatus("Please enter a valid deployed contract address.");
            return;
        }
        try {
            setStatus("Sending transaction to increment...");
            const contract = await getContract();
            const tx = await contract.increment();
            setStatus("Transaction pending... Please wait.");
            await tx.wait();
            setStatus("Counter successfully incremented!");
            handleGet(); // Auto refresh
        } catch (err) {
            console.error(err);
            setStatus(`Increment failed: ${err.message || err}`);
        }
    };

    // Listen for account updates
    useEffect(() => {
        if (window.ethereum) {
            window.ethereum.request({ method: "eth_accounts" })
                .then((accounts) => {
                    if (accounts && accounts.length > 0) setWalletAddress(accounts[0]);
                })
                .catch((err) => console.error("Error checking accounts", err));

            const handleAccounts = (accounts) => {
                setWalletAddress(accounts[0] || "");
            };

            if (window.ethereum.on) {
                window.ethereum.on("accountsChanged", handleAccounts);
            }

            return () => {
                if (window.ethereum.removeListener) {
                    window.ethereum.removeListener("accountsChanged", handleAccounts);
                }
            };
        }
    }, []);

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                {/* Header */}
                <div style={styles.header}>
                    <div>
                        <h1 style={styles.title}>Counter dApp</h1>
                        <span style={styles.subtitle}>Pharos Atlantic Testnet Quickstart (Hardhat)</span>
                    </div>
                    <button 
                        onClick={connectWallet} 
                        style={walletAddress ? styles.walletBadge : styles.connectBtn}
                    >
                        {walletAddress 
                            ? `${walletAddress.substring(0, 6)}...${walletAddress.substring(38)}` 
                            : "Connect Wallet"}
                    </button>
                </div>

                {/* Contract Input */}
                <div style={styles.formGroup}>
                    <label style={styles.label}>Contract Address</label>
                    <input
                        type="text"
                        value={contractAddress}
                        onChange={(e) => setContractAddress(e.target.value)}
                        style={styles.input}
                    />
                </div>

                {/* Display Value */}
                <div style={styles.displayCard}>
                    <div style={styles.displayLabel}>On-chain Counter Value</div>
                    <div style={styles.displayValue}>{counter}</div>
                    <button onClick={handleGet} style={styles.refreshBtn}>Refresh Value</button>
                </div>

                {/* Actions */}
                <div style={styles.actions}>
                    <div style={{ display: "flex", gap: "10px" }}>
                        <input
                            type="number"
                            placeholder="New Value"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            style={{ ...styles.input, flex: 1 }}
                        />
                        <button onClick={handleSet} style={styles.primaryBtn}>Set Value</button>
                    </div>

                    <button onClick={handleIncrement} style={styles.accentBtn}>
                        🚀 Increment Counter (+1)
                    </button>
                </div>

                {/* Status Bar */}
                <div style={styles.statusBar}>
                    <strong>Status:</strong> {status}
                </div>
            </div>
        </div>
    );
}

// Sleek and simple inline styles for quick development template
const styles = {
    container: {
        maxWidth: "600px",
        margin: "80px auto",
        padding: "0 20px",
        fontFamily: "'Inter', sans-serif",
    },
    card: {
        background: "rgba(30, 41, 59, 0.5)",
        backdropFilter: "blur(12px)",
        WebkitBackdropFilter: "blur(12px)",
        border: "1px solid rgba(255, 255, 255, 0.08)",
        borderRadius: "16px",
        padding: "30px",
        boxShadow: "0 20px 40px rgba(0, 0, 0, 0.4)",
    },
    header: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
        paddingBottom: "18px",
        marginBottom: "22px",
    },
    title: {
        fontFamily: "'Outfit', sans-serif",
        fontSize: "1.8rem",
        fontWeight: "800",
        background: "linear-gradient(135deg, #c084fc 0%, #6366f1 100%)",
        WebkitBackgroundClip: "text",
        WebkitTextFillColor: "transparent",
        margin: 0,
    },
    subtitle: {
        fontSize: "0.85rem",
        color: "#64748b",
    },
    connectBtn: {
        background: "linear-gradient(135deg, #6366f1, #4f46e5)",
        border: "none",
        color: "#fff",
        padding: "8px 16px",
        borderRadius: "8px",
        fontWeight: "600",
        cursor: "pointer",
        transition: "opacity 0.2s",
    },
    walletBadge: {
        background: "rgba(99, 102, 241, 0.12)",
        border: "1px solid rgba(99, 102, 241, 0.25)",
        color: "#818cf8",
        padding: "8px 16px",
        borderRadius: "8px",
        fontWeight: "600",
        fontFamily: "monospace",
        cursor: "default",
    },
    formGroup: {
        display: "flex",
        flexDirection: "column",
        gap: "6px",
        marginBottom: "20px",
    },
    label: {
        fontSize: "0.75rem",
        fontWeight: "700",
        color: "#94a3b8",
        textTransform: "uppercase",
        letterSpacing: "0.05em",
    },
    input: {
        background: "rgba(15, 23, 42, 0.6)",
        border: "1px solid rgba(255, 255, 255, 0.08)",
        borderRadius: "8px",
        padding: "10px 14px",
        color: "#f8fafc",
        fontSize: "0.9rem",
        outline: "none",
    },
    displayCard: {
        background: "rgba(15, 23, 42, 0.4)",
        border: "1px solid rgba(255, 255, 255, 0.04)",
        borderRadius: "10px",
        padding: "18px",
        textAlign: "center",
        marginBottom: "20px",
        position: "relative",
    },
    displayLabel: {
        fontSize: "0.8rem",
        color: "#94a3b8",
        marginBottom: "6px",
    },
    displayValue: {
        fontFamily: "'Outfit', sans-serif",
        fontSize: "2rem",
        fontWeight: "800",
        color: "#f8fafc",
        marginBottom: "8px",
    },
    refreshBtn: {
        background: "transparent",
        border: "1px solid rgba(255, 255, 255, 0.15)",
        color: "#94a3b8",
        padding: "4px 10px",
        borderRadius: "6px",
        fontSize: "0.75rem",
        cursor: "pointer",
        transition: "all 0.2s",
    },
    actions: {
        display: "flex",
        flexDirection: "column",
        gap: "12px",
        marginBottom: "20px",
    },
    primaryBtn: {
        background: "linear-gradient(135deg, #6366f1, #4f46e5)",
        border: "none",
        color: "#fff",
        padding: "10px 18px",
        borderRadius: "8px",
        fontWeight: "600",
        cursor: "pointer",
    },
    accentBtn: {
        background: "linear-gradient(135deg, #ec4899, #db2777)",
        border: "none",
        color: "#fff",
        padding: "12px 18px",
        borderRadius: "8px",
        fontWeight: "700",
        cursor: "pointer",
        textAlign: "center",
    },
    statusBar: {
        fontSize: "0.8rem",
        color: "#94a3b8",
        background: "rgba(15, 23, 42, 0.6)",
        padding: "8px 12px",
        borderRadius: "6px",
        border: "1px solid rgba(255, 255, 255, 0.05)",
        wordBreak: "break-all",
    }
};

export default App;

```

---

### File: `hardhat/app/main.jsx`

```javascript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './app.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
)

```

---

### File: `hardhat/contract/.env`

```
PHAROS_MAINNET_RPC_URL="https://pharos-mainnet.g.alchemy.com/v2/ecck2p9w9oZkTCfiXjl3w"
PHAROS_ATLANTIC_RPC_URL="https://pharos-atlantic.g.alchemy.com/v2/ecck2p9w9oZkTCfiXjl3w"
PHAROS_MAINNET_CHAIN_ID="688688"
PHAROS_ATLANTIC_CHAIN_ID="688689"
PRIVATE_KEY=4f34a2df8cc58b9fe7a8f7a807875f02068b28652b2a74df5b760685e88a5a41

```

---

### File: `hardhat/contract/.gitignore`

```
# Compiler files
cache/
out/

# Ignores development broadcast logs
!/broadcast
/broadcast/*/31337/
/broadcast/**/dry-run/

# Docs
docs/

# Dotenv file
.env
package-lock.json
node_modules/

node_modules
.env

# Hardhat files
/cache
/artifacts

# TypeChain files
/typechain
/typechain-types

# solidity-coverage files
/coverage
/coverage.json

# Hardhat Ignition default folder for deployments against a local node
ignition/deployments/

```

---

### File: `hardhat/contract/README.md`

```markdown
# Sample Hardhat Project

This project demonstrates a basic Hardhat use case. It comes with a sample contract, a test for that contract, and a Hardhat Ignition module that deploys that contract.

Try running some of the following tasks:

```shell
npx hardhat help
npx hardhat test
REPORT_GAS=true npx hardhat test
npx hardhat node
npx hardhat ignition deploy ./ignition/modules/Counter.js
```

```

---

### File: `hardhat/contract/contracts/Counter.sol`

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Counter {
    uint256 public number;

    function setNumber(uint256 newNumber) public {
        number = newNumber;
    }

    function increment() public {
        number++;
    }

    // Compatibility functions for Simple Storage integration
    function set(uint256 newNumber) public {
        number = newNumber;
    }

    // Get number
    function get() public view returns (uint256) {
        return number;
    }
}

```

---

### File: `hardhat/contract/hardhat.config.js`

```javascript
require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28",
  networks: {
    pharos: {
      url: [vars.get("PHAROS_RPC_URL")],
      accounts: [vars.get("PRIVATE_KEY")],
    },
  },
};

```

---

### File: `hardhat/contract/ignition/modules/Counter.js`

```javascript
// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules");

module.exports = buildModule("CounterModule", (m) => {
  const counter = m.contract("Counter", []);

  return { counter };
});


```

---

### File: `hardhat/contract/package.json`

```json
{
  "name": "contract",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC",
  "description": "",
  "devDependencies": {
    "@nomicfoundation/hardhat-toolbox": "^5.0.0",
    "hardhat": "^2.22.17"
  }
}

```

---

### File: `hardhat/index.html`

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Simple Storage & Counter dApp | Pharos Atlantic</title>
    <!-- Premium Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #0b0f19;
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,0.3) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(271,76%,53%,0.15) 0, transparent 50%),
                radial-gradient(at 50% 100%, hsla(224,71%,4%,1) 0, transparent 100%);
            background-attachment: fixed;
            color: #f8fafc;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
        }
    </style>
</head>

<body>
    <div id="root"></div>
    <script type="module" src="/app/main.jsx"></script>
</body>

</html>

```

---

### File: `hardhat/package.json`

```json
{
  "name": "dapp-hardhat",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "ethers": "^5.7.2",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.4.1"
  }
}

```

---

### File: `hardhat/vite.config.js`

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
});

```

---
