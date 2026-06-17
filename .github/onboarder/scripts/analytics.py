import sys
import os
import datetime
import argparse
import json
import requests

def load_env(env_path=".env"):
    """Manually parse .env file to avoid external python-dotenv dependency issues."""
    # Search current directory, then check parent directory if not found
    search_paths = [env_path, os.path.join("..", env_path), os.path.join("../..", env_path)]
    for path in search_paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        # Remove whitespace and surrounding quotes
                        key = key.strip()
                        val = val.strip().strip('"').strip("'")
                        os.environ[key] = val
            break

class PharosBlockchainStats:
    def __init__(self, api_key: str, network: str = "pharos-atlantic-testnet"):
        self.api_key = api_key
        # SocialScan API URL pattern: https://api.socialscan.io/{network}/v1/developer/api
        self.base_url = f"https://api.socialscan.io/{network}/v1/developer/api"
        
    def _fetch_data(self, action: str, start_date: str, end_date: str, sort: str = "asc"):
        params = {
            "module": "stats",
            "action": action,
            "startdate": start_date,  # Format: yyyy-MM-dd
            "enddate": end_date,      # Format: yyyy-MM-dd
            "sort": sort,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1":
                return data.get("result", [])
            else:
                # Fallback for mock/offline testing if API returns error
                return {"error": f"API Error: {data.get('message')} - {data.get('result')}"}
        except Exception as e:
            return {"error": f"HTTP request failed: {str(e)}"}

    def get_stats(self, action: str, start_date: str, end_date: str):
        return self._fetch_data(action, start_date, end_date)


def parse_and_format_data(data, action):
    """Robust parser that handles different Etherscan/SocialScan daily metrics schemas."""
    if isinstance(data, dict) and "error" in data:
        return None, data["error"]
        
    if not isinstance(data, list) or len(data) == 0:
        return None, "No daily stats records returned from the API."

    parsed_records = []
    
    # Map actions to standard returned field names
    val_keys = {
        "dailytx": ["transactionCount", "tx_count", "value", "count"],
        "dailynewaddress": ["newAddressCount", "new_addresses", "value", "count"],
        "dailytxnfee": ["totalFee", "txnFee", "fee", "value"],
        "dailynetutilization": ["networkUtilization", "utilization", "value"]
    }
    
    target_keys = val_keys.get(action, ["value", "count"])

    for record in data:
        # 1. Parse date
        # 1. Parse date case-insensitively
        date_str = None
        for k, v in record.items():
            if k.lower() in ["utcdate", "date", "timestamp"]:
                date_str = v
                break
                
        if not date_str:
            continue
            
        # 2. Parse value case-insensitively using lower_targets
        val = None
        lower_record = {k.lower(): v for k, v in record.items()}
        lower_targets = [k.lower() for k in target_keys]
        for key in lower_targets:
            if key in lower_record:
                try:
                    val = float(lower_record[key])
                    break
                except (ValueError, TypeError):
                    continue
        
        if val is None:
            # Try to grab whatever value is inside the dictionary except date/timestamp keys
            for key, v in record.items():
                if key.lower() not in ["utcdate", "date", "timestamp", "unixtimestamp"]:
                    try:
                        val = float(v)
                        break
                    except (ValueError, TypeError):
                        continue
        
        if val is None:
            val = 0.0
            
        parsed_records.append((date_str, val))
        
    return parsed_records, None



def supports_color():
    """Returns True if the running system supports ANSI color codes."""
    if "NO_COLOR" in os.environ:
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

def generate_ascii_chart(records, max_width=40, supports_color=False):
    """Generates a clean text-based horizontal bar chart of the timeseries trends."""
    if not records:
        return "No data to plot."
        
    max_val = max(r[1] for r in records)
    if max_val == 0:
        max_val = 1
        
    chart_lines = []
    CYAN = "\033[96m" if supports_color else ""
    RESET = "\033[0m" if supports_color else ""
    
    for date_str, val in records:
        bar_len = int((val / max_val) * max_width)
        bar = "■" * bar_len
        # Format floating values nicely if they have decimals
        val_str = f"{int(val)}" if val.is_integer() else f"{val:.4f}"
        chart_lines.append(f"{date_str} | {CYAN}{bar}{RESET} ({val_str})")
        
    return "\n".join(chart_lines)


def main():
    load_env()
    
    parser = argparse.ArgumentParser(description="Pharos Blockchain Stats Analyst CLI")
    parser.add_argument("--action", "-a", default="dailytx", choices=["dailytx", "dailynewaddress", "dailytxnfee", "dailynetutilization"], help="API stats action to perform")
    parser.add_argument("--network", "-n", default="pharos-atlantic-testnet", help="SocialScan target network")
    parser.add_argument("--days", "-d", type=int, default=7, help="Number of past days to query")
    parser.add_argument("--start-date", "-s", help="Explicit start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", "-e", help="Explicit end date (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON results")
    
    args = parser.parse_args()
    
    api_key = os.getenv("SOCIALSCAN_API")
    if not api_key:
        print("ERROR: SOCIALSCAN_API key is missing. Please register at https://thehemera.gitbook.io/explorer-api and add it to your .env file.")
        sys.exit(1)
        
    # Calculate dates if not explicitly provided
    if args.start_date and args.end_date:
        start_str = args.start_date
        end_str = args.end_date
    else:
        end_dt = datetime.date.today()
        start_dt = end_dt - datetime.timedelta(days=args.days)
        start_str = start_dt.strftime("%Y-%m-%d")
        end_str = end_dt.strftime("%Y-%m-%d")

    # Fetch stats
    stats_api = PharosBlockchainStats(api_key=api_key, network=args.network)
    raw_data = stats_api.get_stats(args.action, start_str, end_str)
    
    if args.json:
        print(json.dumps(raw_data, indent=2))
        return

    # Parse and analyze
    records, error = parse_and_format_data(raw_data, args.action)
    if error:
        # If API failed or is offline, generate a mock dataset to allow offline testing
        # as requested for a smooth developer onboarding flow
        mock_data = []
        start_dt = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
        end_dt = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()
        delta = end_dt - start_dt
        
        # Consistent seed-like generation for mock data
        for i in range(delta.days + 1):
            curr_date = start_dt + datetime.timedelta(days=i)
            # Create a mock wave trend
            if args.action == "dailytx":
                val = 5.0 + (i % 3) * 4.0 + (i % 5) * 2.0
            elif args.action == "dailynewaddress":
                val = 2.0 + (i % 2) * 3.0
            elif args.action == "dailytxnfee":
                val = 0.001 * (5.0 + (i % 4) * 2.0)
            else:
                val = 12.5 + (i % 3) * 5.0
            mock_data.append((curr_date.strftime("%Y-%m-%d"), val))
            
        records = mock_data
        is_mock = True
    else:
        is_mock = False

    # Perform calculations
    total_val = sum(r[1] for r in records)
    avg_val = total_val / len(records) if records else 0
    min_rec = min(records, key=lambda x: x[1]) if records else ("N/A", 0.0)
    max_rec = max(records, key=lambda x: x[1]) if records else ("N/A", 0.0)

    # Estimate block counts (Mock blocks calculation based on tx throughput)
    # Average block contains ~15 transactions on testnet.
    if args.action == "dailytx":
        estimated_blocks = max(1, int(total_val / 15))
        block_str = f" in {estimated_blocks} blocks"
    else:
        block_str = ""

    # Human-friendly metric names
    metric_names = {
        "dailytx": "Transactions",
        "dailynewaddress": "New Addresses",
        "dailytxnfee": "Transaction Fees (PHRS/PROS)",
        "dailynetutilization": "Network Gas Utilization (%)"
    }
    m_name = metric_names.get(args.action, args.action)

    # Set up styling constants
    if supports_color():
        CYAN = "\033[96m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        BOLD = "\033[1m"
        RESET = "\033[0m"
    else:
        CYAN = GREEN = YELLOW = RED = BOLD = RESET = ""

    header = "PHAROS DAILY BLOCKCHAIN STATS REPORT"
    print(f"{CYAN}{BOLD}╔{'═' * 52}╗{RESET}")
    print(f"{CYAN}{BOLD}║{header.center(52)}║{RESET}")
    print(f"{CYAN}{BOLD}╚{'═' * 52}╝{RESET}")
    
    if is_mock:
        mock_msg = "[⚠️ OFFLINE MODE: Using local mock data due to API error]"
        print(f"{YELLOW}{BOLD}{mock_msg.center(54)}{RESET}")
        
    print(f"{BOLD}Network:{RESET}  {GREEN}{args.network}{RESET}")
    print(f"{BOLD}Metric:{RESET}   {GREEN}{m_name}{RESET}")
    print(f"{BOLD}Query:{RESET}    Last {len(records)} days ({start_str} to {end_str})")
    print(f"{CYAN}{'-' * 54}{RESET}")
    print(f"📊 {BOLD}Summary Analysis:{RESET}")
    print(f"  - Total {m_name}: {GREEN}{BOLD}{total_val:.4f}{RESET}".replace(".0000", "") + block_str)
    print(f"  - Daily Average: {CYAN}{avg_val:.4f}{RESET}".replace(".0000", ""))
    print(f"  - Minimum Value: {YELLOW}{min_rec[1]:.4f}{RESET} ({min_rec[0]})".replace(".0000", ""))
    print(f"  - Maximum Value: {GREEN}{BOLD}{max_rec[1]:.4f}{RESET} ({max_rec[0]})".replace(".0000", ""))
    print(f"{CYAN}{'-' * 54}{RESET}")
    print(f"📈 {BOLD}Timeseries Trend Chart:{RESET}")
    print(generate_ascii_chart(records, supports_color=supports_color()))
    print(f"{CYAN}{'=' * 54}{RESET}")

if __name__ == "__main__":
    main()