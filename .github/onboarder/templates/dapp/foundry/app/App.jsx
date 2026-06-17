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