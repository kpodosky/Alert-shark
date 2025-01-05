# -*- coding: UTF-8 -*-
import requests
import time
from datetime import datetime

class BitcoinWhaleTracker:
    def __init__(self, min_btc=10):
        self.base_url = "https://blockchain.info"
        self.min_btc = min_btc
        self.satoshi_to_btc = 100000000  # 1 BTC = 100,000,000 satoshis
        
    def get_latest_block(self):
        """Get the latest block hash"""
        try:
            response = requests.get(f"{self.base_url}/latestblock")
            return response.json()['hash']
        except Exception as e:
            print(f"Error getting latest block: {e}")
            return None

    def get_block_transactions(self, block_hash):
        """Get all transactions in a block"""
        try:
            response = requests.get(f"{self.base_url}/rawblock/{block_hash}")
            return response.json()['tx']
        except Exception as e:
            print(f"Error getting block transactions: {e}")
            return []

    def process_transaction(self, tx):
        """Process a single transaction and return if it meets criteria"""
        # Calculate total input value
        input_value = sum(inp.get('prev_out', {}).get('value', 0) for inp in tx.get('inputs', []))
        btc_value = input_value / self.satoshi_to_btc
        
        # Only process transactions over minimum BTC threshold
        if btc_value < self.min_btc:
            return None
            
        # Get the primary sender (first input address)
        sender = tx.get('inputs', [{}])[0].get('prev_out', {}).get('addr', 'Unknown')
        
        # Get the primary receiver (first output address)
        receiver = tx.get('out', [{}])[0].get('addr', 'Unknown')
        
        # Calculate fee
        output_value = sum(out.get('value', 0) for out in tx.get('out', []))
        fee = (input_value - output_value) / self.satoshi_to_btc
        
        return {
            'timestamp': datetime.fromtimestamp(tx.get('time', 0)).strftime('%Y-%m-%d %H:%M:%S'),
            'transaction_hash': tx.get('hash', 'Unknown'),
            'sender': sender,
            'receiver': receiver,
            'btc_volume': round(btc_value, 4),
            'fee_btc': round(fee, 8),
            'usd_value': self.get_usd_value(btc_value)
        }

    def get_usd_value(self, btc_amount):
        """Get USD value of BTC amount"""
        try:
            response = requests.get(f"{self.base_url}/ticker")
            usd_rate = float(response.json()['USD']['last'])
            return round(btc_amount * usd_rate, 2)
        except Exception as e:
            print(f"Error getting USD value: {e}")
            return None

    def print_transaction(self, tx):
        """Print transaction in formatted alert style"""
        # Clear line and move cursor to beginning
        print('\033[2K\033[G', end='')
        
        # Print formatted alert
        print("\n" + "=" * 70)
        print("\033[94m🚨🚨🚨 Bitcoin fx transfer Alert !\033[0m")
        print(f"Hash: {tx['transaction_hash']}")
        print(f"\033[94m{tx['btc_volume']} BTC (${tx['usd_value']:,.2f})", end='')
        print(f"        Fee: {tx['fee_btc']} BTC\033[0m")
        print(f"From: {tx['sender']}")
        print(f"To: {tx['receiver']}")
        print("=" * 70 + "\n")

    def track_whale_transactions(self):
        """Main method to track whale transactions"""
        print(f"Tracking Bitcoin transactions over {self.min_btc} BTC...")
        while True:
            block_hash = self.get_latest_block()
            if not block_hash:
                time.sleep(60)
                continue
                
            transactions = self.get_block_transactions(block_hash)
            for tx in transactions:
                whale_tx = self.process_transaction(tx)
                if whale_tx:
                    self.print_transaction(whale_tx)
            
            time.sleep(60)  # Wait for new block

if __name__ == "__main__":
    tracker = BitcoinWhaleTracker(min_btc=10)  # Track transactions over 10 BTC
    tracker.track_whale_transactions()