# Developer Onboarding Guide: The Pharos Network

Welcome to the **Pharos Network** engineering team! This document provides a highly technical, deep-dive summary of the Pharos architecture, its primary protocol innovations, and execution layers. This guide is designed to get you up to speed on what makes Pharos unique and how to reason about system performance and application development on our network.

---

## 1. Executive Overview

Pharos Network is an ultra-fast, EVM-compatible, internet-scale **Layer-1 blockchain** specifically optimized for **RealFi (Real-World Finance)**, Real-World Asset (RWA) tokenization, stablecoin infrastructure, and high-throughput decentralized payments. 

Founded by former blockchain executives from Ant Group (including the former CTO of Ant Chain and the Chief Security Officer of Ant Financial’s Web3 division), Pharos was engineered to solve the structural limitations of legacy Layer-1 chains—namely state bloat, rigid single-threaded execution, high storage I/O bottlenecks, and lack of institutional compliance hooks.

### Core Metrics & Capabilities
* **Throughput:** Up to 50,000+ Transactions Per Second (TPS) in production (with prototypes benchmarking over 130,000 TPS on a 100-node global testbed).
* **Finality:** Sub-second / 1-second deterministic finality.
* **Storage Efficiency:** Up to an 80.3% reduction in storage costs and a 15.8x improvement in data I/O throughput compared to traditional architectures.
* **Compatibility:** Dual execution environment supporting both **EVM** (Solidity/Vyper) and **WASM** (Rust, C++, Go).

---

## 2. Structural Layer Architecture

Unlike monolithic blockchains or fragmented L2 modular frameworks, Pharos relies on a highly integrated **Modular Full-Stack Parallel Architecture** divided into three distinct conceptual layers:

```
+-------------------------------------------------------------+
|                     L1-EXTENSION LAYER                      |
|      (Special Processing Networks - SPNs, AI, ZK-KYC)       |
+-------------------------------------------------------------+
|                      L1-CORE LAYER                          |
|     (Pharos Consensus, Pipelining, Dual EVM+WASM VM)        |
+-------------------------------------------------------------+
|                      L1-BASE LAYER                          |
|     (Pharos Store, Hardware Acceleration, Data Avail.)      |
+-------------------------------------------------------------+
```

### L1-Base: The Data and Storage Foundation
Handles hardware acceleration, fundamental data availability, and the native **Pharos Store** engine. It optimizes the physical and cryptographic storage of the ledger to ensure that disk I/O does not bottleneck execution.

### L1-Core: The Consensus and Execution Engine
Responsible for state transition verification, parallel transaction handling, and execution pipelines. It houses the consensus mechanism and the dual-virtual-machine runtimes.

### L1-Extension: The Application and Specialization Layer
Facilitates modular custom environments, privacy-preserving computation, zero-knowledge compliance frameworks (ZK-KYC/AML), and interoperability with external ecosystems.

---

## 3. Core Technical Differentiators

As a developer on Pharos, you will interact with five foundational architectural pillars that distinguish our stack from networks like Ethereum or Solana:

### A. Deep Parallelism Architecture (DP4 / DP5)
Pharos breaks the traditional sequential execution model using a multi-tier **Degree of Parallelism (DP)** framework, targeting DP4 in its production environment. This combines:
* **Parallel Transaction Execution:** Inspecting transaction dependencies dynamically to execute independent transactions concurrently across multi-core processors without state conflicts.
* **Full-Lifecycle Asynchronous Pipelining:** Splitting the traditional block processing loop into 6 independent parallel stages (e.g., fetch, decode, execute, state-root compute, commit). This isolates CPU, memory, and disk I/O operations into individual, continuous assembly lines.

### B. Dual VM Execution Environment
Pharos eliminates the trade-off between standard tooling and performance by running two virtual machines simultaneously:
1.  **EVM Component:** Offers complete, out-of-the-box compatibility with the Ethereum developer toolchain (Hardhat, Foundry, Remix, ethers.js). You can deploy existing Solidity smart contracts without modification.
2.  **WASM Component:** Allows high-performance, complex logic to be compiled to WebAssembly from systems languages like **Rust, C++, and Go**. 

Both VMs share a unified state space, allowing seamless cross-calling and structural composability between an EVM contract and a WASM contract.

### C. Pharos Store (Native Storage Engine)
Traditional EVM chains rely on a multi-layer storage paradigm (e.g., Merkle Patricia Tries mapped onto a key-value database like LevelDB or RocksDB). This causes massive read/write amplification ("state bloat"). 

Pharos Store replaces this entirely with a blockchain-native storage architecture utilizing:
* **Delta Encoding:** Only recording state mutations rather than entire data blocks.
* **Version Addressing:** Direct indexing via state versioning instead of expensive cryptographic hash lookups.
* **ADS Pushdown:** Authenticated Data Structure logic is pushed directly into the physical database layer, achieving a **15.8x higher I/O throughput** and slicing storage footprints by **80%**.

### D. Pharos Consensus Engine
Moving away from rigid, single-proposer block schedules that suffer under wide-area network latency, the Pharos Consensus protocol allows **all validators to propose blocks simultaneously**. It adapts dynamically to real-world network delays and completely eliminates single-proposer bottlenecks, paving the way for sub-second deterministic settlement.

### E. Special Processing Networks (SPNs)
SPNs are modular, highly specialized subnetworks designed for resource-heavy computing constraints (e.g., decentralized AI models, ZK acceleration, FHE, and Trusted Execution Environments). 
* **Security:** Multi-asset restaking mechanics allow validators to restake their `$PROS` (or native liquid assets) directly into specific SPNs to back their computational integrity.
* **Interoperability:** SPNs maintain near-instantaneous, trustless cross-network communication primitives back to the L1-Core layer.

---

## 4. Native Token Architecture (`$PROS` / `$PHRS`)

The network relies on a native utility asset (referred to as `$PROS` on mainnet, or `$PHRS` during testnet phases) which anchors the economic and cryptoeconomic security design.

* **Gas and Computations:** Standard EVM/WASM metered executions and data writes consume native gas fees.
* **Staking and Security:** Network validation runs on a Proof-of-Stake (PoS) consensus mechanism.
* **SPN Economic Security:** Used as the base asset for native restaking validation across heterogeneous hardware networks.
* **Supply Discipline:** Employs a phased inflation schedule (e.g., 0% staking inflation during the initial launch and price-discovery months) to prioritize early network health and long-term supply preservation.


---
## 5. Pharos Networks
* **Pharos Pacific Mainnet**

The **Pacific Mainnet** is the production environment for the Pharos Network, running the live consensus protocol for high-throughput RealFi, stablecoin operations, and institutional-grade RWA transactions utilizing the native `$PROS` asset.

### Network Parameters
| Parameter | Configuration Value |
| :--- | :--- |
| **Network Name** | Pharos Pacific Mainnet |
| **Chain ID (Decimal)** | `1672` |
| **Chain ID (Hex)** | `0x688` |
| **Currency Symbol** | `PROS` |
| **Currency Decimals** | `18` |
| **Primary RPC URL** | `https://rpc.pharos.xyz` |
| **Block Explorer URL** | `https://www.pharosscan.xyz` |


* **Pharos Atlantic Testnet**

The **Atlantic Testnet** is the core sandbox network for application testing, consensus validation, and iterative smart contract deployments. Developers should use this ecosystem to build, test, and audit their applications using testnet `$PHRS` tokens prior to staging production mainnet versions.

### Network Parameters
| Parameter | Configuration Value |
| :--- | :--- |
| **Network Name** | Pharos Atlantic Testnet |
| **Chain ID (Decimal)** | `688689` |
| **Chain ID (Hex)** | `0xa8231` |
| **Currency Symbol** | `PHRS` |
| **Currency Decimals** | `18` |
| **Primary RPC URL** | `https://atlantic.dplabs-internal.com` |
| **Alternative RPC URL** | `https://rpc.evm.pharos.testnet.cosmostation.io` |
| **Block Explorer URL** | `https://atlantic.pharosscan.xyz` |

---

## 6. Developer Quickstart Ecosystem & Tooling

As an onboarding developer, your workflow will map closely to your existing Web3 patterns, with minor optimizations for our parallel architecture:

### 1. Connecting to the Network
Pharos supports standard JSON-RPC namespaces (`eth_*`). You can connect standard non-custodial Web3 environments (MetaMask, OKX Wallet, Bitget Wallet) by pointing them to the Pharos Gateway endpoints.

### 2. Smart Contract Development
* **For Solidity Devs:** Use **Foundry** or **Hardhat** exactly as you would on Ethereum. When deploying, parallel transaction routing and optimization happen automatically underneath the RPC layer through "parallel hints."
* **For Performance-Critical Logic:** Utilize the WASM compilation toolchains to design highly complex decentralized risk engines, order books, or automated compliance/KYC modules in Rust.

### 3. Key Protocols and Integrations
Keep an eye out for our native ecosystem primitives integrated directly at the base layer:
* **Native Lending Architecture:** Built-in collaborations (such as with Morpho-based designs) that natively provision institutional lending against tokenized real-world assets.
* **Compliance Primitives:** Cryptographically secure, ZK-proof-based KYC and AML layers built natively into the L1-Extension layer to ensure institution-grade regulatory capabilities without compromising onchain privacy.


Vist https://docs.pharos.xyz/ or ask me if you would like a more detailed overview of the pharos network or specific aspects of it.