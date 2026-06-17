---
name: pharos-onboarder-fast
description: >
  Automated, non-interactive, ultra-fast setup skill for the Pharos blockchain network.
  Triggers whenever the user or another agent requests "onboarder fast", "pharos fast setup",
  "fast onboard", "quick setup pharos", or "onboarder_v2".
  This skill instructs the agent to run the system setup, install dependencies, scaffold
  the project workspace, configure credentials, and verify RPC queries in sequence
  without interactive prompts or user dialogues.
---

# Pharos Automated Fast Onboarder (onboarder_v2) ⚡

This skill is optimized for AI agents and developer CLIs to execute an **automated, zero-interactive, ultra-fast bootstrap** of the Pharos Network environment in the local project workspace. It eliminates teaching dialogues and executes all diagnostic, scaffolding, and verification steps programmatically.

> **⚠️ Agent Portability Note:** The templates in this skill are located relative to the directory of this skill file. When executing copy commands on behalf of the user, resolve paths relative to this skill file's directory (e.g., `<skill_dir>/templates/...`).

---

## 📋 Execution Order (Agent Instructions)

The executing agent must proceed through the following steps in sequence, executing the command payloads automatically and writing files on behalf of the user.

---

### Step 1: Host Diagnostic Scan
Run checks to verify that the environment meets package requirements.
```bash
npm -v
yarn -v
git --version
```
*   **Action Policy:**
    - If `npm` is missing or version `< 11.13.0`, immediately run: `npm install -g npm@latest`
    - If `yarn` is missing, install it: `npm install --global yarn@1`

---

### Step 2: Initialize Project Folder
Scaffold the base JavaScript quickstart workspace.
```bash
mkdir -p pharos-api-quickstart && cd pharos-api-quickstart
npm init --yes
```

---

### Step 3: Install Required Dependencies
Install the standard networking and config loading utilities silently.
```bash
cd pharos-api-quickstart
npm install axios dotenv
```

---

### Step 4: Configure Secrets & Credentials
1.  Check the parent project directory or active terminal environment variables for existing keys:
    - `PHAROS_ATLANTIC_RPC_URL`
    - `PHAROS_MAINNET_RPC_URL`
    - `PRIVATE_KEY`
2.  Write the `.env` configuration file inside `pharos-api-quickstart`:
    ```bash
    cat << 'EOF' > .env
    PHAROS_MAINNET_RPC_URL=https://pharos-mainnet.g.alchemy.com/v2/abc123yourkey
    PHAROS_ATLANTIC_RPC_URL=https://rpc.evm.pharos.testnet.cosmostation.io
    PHAROS_MAINNET_CHAIN_ID=1672
    PHAROS_ATLANTIC_CHAIN_ID=688689
    PRIVATE_KEY=your_private_key_here
    EOF
    ```
    *(If system environment keys were detected, automatically replace the placeholder parameters in the `.env` file with the active keys).*
3.  Write `.gitignore` to prevent secret leaks:
    ```bash
    echo ".env" > .gitignore
    echo "node_modules/" >> .gitignore
    ```

---

### Step 5: Write and Execute Verification Script
Scaffold `index.js` to perform a block number RPC call to verify the Pharos connection.

```bash
cat << 'EOF' > index.js
require('dotenv').config();
const axios = require('axios');

const url = process.env.PHAROS_ATLANTIC_RPC_URL || "https://rpc.evm.pharos.testnet.cosmostation.io";

const payload = {
  jsonrpc: '2.0',
  id: 1,
  method: 'eth_blockNumber',
  params: []
};

(async () => {
  try {
    const response = await axios.post(url, payload);
    const blockNumber = parseInt(response.data.result, 16);
    console.log(`STATUS: CONNECTED | BLOCK: ${blockNumber}`);
  } catch (error) {
    console.log(`STATUS: FAILED | ERROR: ${error.message}`);
    process.exit(1);
  }
})();
EOF
```

Execute the verification check:
```bash
node index.js
```

---

### Step 6: Install Official Pharos Skill Engine
Install the standard AI-agent skill suite silently into the project scope to support direct Web3 chat intents:
```bash
npx skills add https://github.com/PharosNetwork/pharos-skill-engine
```

---

### Step 7: Framework Auto-Scaffolding
Inspect the host system to determine the available Solidity compilers/frameworks:
```bash
which forge
```
*   **Scenario A: Forge is available (Foundry Preferential Setup):**
    Copy the Foundry template directory, and initialize the contracts workspace:
    ```bash
    mkdir -p contract
    cp -r ./templates/tokens/foundry/* contract/
    cd contract/contracts
    forge install OpenZeppelin/openzeppelin-contracts --no-git
    ```
*   **Scenario B: Forge is NOT available (Hardhat Fallback Setup):**
    Copy the Hardhat template directory, and install requirements:
    ```bash
    mkdir -p contract
    cp -r ./templates/tokens/hardhat/* contract/
    cd contract
    npm install
    ```

---

### Step 8: Execution Complete Summary
Print a standardized JSON log summarizing the bootstrap state for the caller agent:
```json
{
  "status": "COMPLETED",
  "project_dir": "pharos-api-quickstart",
  "dependencies": ["axios", "dotenv"],
  "skills_engine": "installed",
  "framework": "foundry/hardhat configured"
}
```