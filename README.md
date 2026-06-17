# Pharos Network Onboarder Skills 🚀

A suite of developer onboarding tools and automated bootstrapping skills for the **Pharos Network**, designed for both human developers and autonomous AI agents. 

This repository contains two distinct skill packages that can be added to your workspace or your AI agent's configuration:
1. **Pharos Interactive Onboarder (`onboarder`)**: A lively, step-by-step developer tutorial guided by an interactive senior dev persona, featuring smart contract activities (Foundry & Hardhat) and a SocialScan daily analytics dashboard.
2. **Pharos Fast Onboarder (`onboarder_fast`)**: A zero-interactive, ultra-fast environment bootstrapped layout optimized for AI-to-AI system configuration and automated toolchain environments.

---

## 📂 Repository Structure

```text
pharos/
├── .github/
│   ├── onboarder/                 # Interactive Onboarder Skill
│   │   ├── SKILL.md               # Main instruction manifest
│   │   ├── templates/             # Code templates (dapp, tokens, nft) for Foundry/Hardhat
│   │   └── scripts/
│   │       ├── analytics.py       # SocialScan metrics analytics client
│   │       └── requirements.txt   # Python dependency config
│   └── onboarder_fast/            # Fast/Automated Onboarder Skill
│       ├── SKILL.md               # Main instruction manifest
│       └── templates/             # Isolated copy of templates for agent scaffolding
├── rough_onboarder.md             # Developer-facing detailed guide markdown
├── README.md                      # Repository overview (this file)
└── deploy_instructions.md         # Deployment and publishing reference
```

---

## 🛠️ Skills Breakdown

### 1. Interactive Onboarder (`.github/onboarder`)
*   **Best For**: Human developers setting up Pharos for the first time.
*   **Triggers**: `onboarder`, `onboard pharos`, `start pharos setup`, `pharos quickstart`, `pharos RPC setup`, `pharos wallet setup`.
*   **Shortcut Commands**:
    *   `onboarder pharos skills`: Jump directly to the **On-chain Skills Crash Course**.
    *   `onboarder pharos stats` / `onboarder stats`: Jump directly to **SocialScan Daily Analytics**.
    *   `onboarder foundry`: Jump directly to the **Foundry Toolchain setup**.
    *   `onboarder hardhat`: Jump directly to the **Hardhat Toolchain setup**.
*   **Key Features**:
    *   Interactive diagnostics (checks node, npm, yarn, git).
    *   Guides claiming testnet `$PHRS` from the faucet and adding Atlantic network manually to wallets.
    *   Teaches how to install and test the official `pharos-skill-engine` to run blockchain actions.
    *   Integrates the daily blockchain stats analyst CLI (`analytics.py`).

### 2. Fast Onboarder (`.github/onboarder_fast`)
*   **Best For**: AI-to-AI integrations, continuous integration (CI) runtimes, or developers who want to bypass dialogue and jump straight into an initialized workspace.
*   **Triggers**: `onboarder fast`, `pharos fast setup`, `fast onboard`, `quick setup pharos`, `onboarder_v2`.
*   **Key Features**:
    *   Zero questions asked. Runs system scan, installs dependencies, scaffolds workspace folder `pharos-api-quickstart`, registers credentials into `.env`, compiles verification scripts, and sets up Foundry/Hardhat contracts instantly.
    *   Returns a standardized JSON confirmation payload upon completion.

---

## 📦 How to Install the Skills

To install either skill to your project workspace or global AI agent directory (e.g. Cline, Claude Code, Codex, Antigravity, OpenClaw):

### Option A: Install Interactive Onboarder
```bash
npx skills add <your-github-repo-url>/.github/onboarder
```

### Option B: Install Fast Onboarder
```bash
npx skills add <your-github-repo-url>/.github/onboarder_fast
```

*Replace `<your-github-repo-url>` with the URL of your published repository (e.g., `https://github.com/username/pharos`).*

---

## 📊 Daily Stats & Analytics (SocialScan API Integration)

The Interactive Onboarder includes a built-in blockchain metrics script that connects with the Hemera SocialScan Explorer API.

### Setup Analytics
1. Get an API key from [SocialScan/Hemera API Portal](https://thehemera.gitbook.io/explorer-api).
2. Save it inside the project `.env` file:
   ```env
   SOCIALSCAN_API=your_socialscan_api_key_here
   ```
3. Run or ask your agent to query:
   ```bash
   python3 ./scripts/analytics.py --action dailytx --days 7
   ```
4. Query in natural language:
   *   *"What is the number of transactions on Pharos Atlantic in the past 3 days?"*
   *   The agent parses the metrics and can generate a custom ASCII trend chart to visualize transaction volume!

---

## 📄 License

This repository is licensed under the MIT License.
