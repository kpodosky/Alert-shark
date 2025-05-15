# -*- coding: UTF-8 -*-
import re
import requests
import time
import os
from datetime import datetime
from collections import defaultdict

class BitcoinWhaleTracker:
    def __init__(self, min_btc=1000):  # Changed from 500 to 1000
        self.base_url = "https://blockchain.info"
        self.min_btc = min_btc
        self.satoshi_to_btc = 100000000
        self.processed_blocks = set()  # Track processed blocks
        self.last_block_height = None  # Track last block height
        
        # Stablecoin addresses for mint/burn detection
        self.stablecoin_addresses = {
           'usdt': {
               'mint_address': '0xdac17f958d2ee523a2206206994597c13d831ec7',
               'burn_address': '0x0000000000000000000000000000000000000000',
               'treasury': '0x5754284f345afc66a98fbb0a0afe71e0f007b949'
            },
            'usdc': {
                'mint_address': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
                'burn_address': '0x0000000000000000000000000000000000000000',
                'treasury': '0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf'
           }
       }
   
        self.address_stats = defaultdict(lambda: {
            'received_count': 0,
            'sent_count': 0,
            'total_received': 0,
            'total_sent': 0,
            'last_seen': None
        })
        
        # Known addresses database (keeping original database)
        self.known_addresses = {
            'binance': {
                'type': 'exchange',
                'addresses': [
                    '3FaA4dJuuvJFyUHbqHLkZKJcuDPugvG3zE',  # Binance Hot Wallet
                    '1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s',  # Binance Cold Wallet
                    '34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo',  # Binance-BTC-2
                    '1LQv8aKtQoiY5M5zkaG8RWL7LMwNzNsLfb',  # Binance-BTC-3
                    '1AC4fMwgY8j9onSbXEWeH6Zan8QGMSdmtA'   # Binance-BTC-4
                ]
            },
            'coinbase': {
                'type': 'exchange',
                'addresses': [
                    '3FzScn724foqFRWvL1kCZwitQvcxrnSQ4K',  # Coinbase Hot Wallet
                    '3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS',  # Coinbase Cold Storage
                    '1CWYTCvwKfH5cWnX3VcAykgTsmjsuB3wXe',  # Coinbase-BTC-2
                    '1FxkfJQLJTXpW6QmxGT6hEo5DtBrnFpM3r',  # Coinbase-BTC-3
                    '1GR9qNz7zgtaW5HwwVpEJWMnGWhsbsieCG'   # Coinbase Prime
                ]
            },
            'grayscale': {
                'type': 'investment',
                'addresses': [
                    'bc1qe7nps5yv7ruc884zscwrk9g2mxvqh7tkxfxwny',
                    'bc1qkz7u6l5c8wqz8nc5yxkls2j8u4y2hkdzlgfnl4'
                ]
            },
            'microstrategy': {
                'type': 'corporate',
                'addresses': [
                    'bc1qazcm763858nkj2dj986etajv6wquslv8uxwczt',
                    'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
                ]
            },
            'blockfi': {
                'type': 'lending',
                'addresses': [
                    'bc1q7kyrfmx49qa7n6g8mvlh36d4w9zf4lkwfg4j5q',
                    'bc1qd73dxk2qfs2x5wv2sesvqrzgx7t5tqt4y5vpym'
                ]
            },
            'celsius': {
                'type': 'lending',
                'addresses': [
                    'bc1q06ymtp6eq27mlz3ppv8z7esc8vq3v4nsjx9eng',
                    'bc1qcex3e38gqh6qnzpn9jth5drgfyh5k9sjzq3rkm'
                ]
            },
            'kraken': {
                'type': 'exchange',
                'addresses': [
                    '3FupZp77ySr7jwoLYEJ9mwzJpvoNBXsBnE',  # Kraken Hot Wallet
                    '3H5JTt42K7RmZtromfTSefcMEFMMe18pMD',  # Kraken Cold Storage
                    '3AfP9N7KNq2pYXiGQdgNJy8SD2Mo7pQKUR',  # Kraken-BTC-2
                    '3E1jkR1PJ8hFUqCkDjimwPoF2bZVrkqnpv'   # Kraken-BTC-3
                ]
            },
            'bitfinex': {
                'type': 'exchange',
                'addresses': [
                    '3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r',  # Bitfinex Hot Wallet
                    '3JZq4atUahhuA9rLhXLMhhTo133J9rF97j',  # Bitfinex Cold Storage
                    '3QW95MafxER9W7kWDcosQNdLk4Z36TYJZL'   # Bitfinex-BTC-2
                ]
            },
            'huobi': {
                'type': 'exchange',
                'addresses': [
                    '3M219KR5vEneNb47ewrPfWyb5jQ2DjxRP6',  # Huobi Hot Wallet
                    '38WUPqGLXphpD1DwkMR8koGfd5UQfRnmrk',  # Huobi Cold Storage
                    '1HckjUpRGcrrRAtFaaCAUaGjsPx9oYmLaZ'   # Huobi-BTC-2
                ]
            },
            'okex': {
                'type': 'exchange',
                'addresses': [
                    '3LQUu4v9z6KNch71j7kbj8GPeAGUo1FW6a',  # OKEx Hot Wallet
                    '3LCGsSmfr24demGvriN4e3ft8wEcDuHFqh',  # OKEx Cold Storage
                    '3FupZp77ySr7jwoLYEJ9mwzJpvoNBXsBnE'   # OKEx-BTC-2
                ]
            },
            'gemini': {
                'type': 'exchange',
                'addresses': [
                    '3P3QsMVK89JBNqZQv5zMAKG8FK3kJM4rjt',  # Gemini Hot Wallet
                    '393HLwqnkrJMxYQTHjWBJPAKC3UG6k6FwB',  # Gemini Cold Storage
                    '3AAzK4Xbu8PTM8AD7gw2XaMZavL6xoKWHQ'   # Gemini-BTC-2
                ]
            },
            'bitstamp': {
                'type': 'exchange',
                'addresses': [
                    '3P3QsMVK89JBNqZQv5zMAKG8FK3kJM4rjt',  # Bitstamp Hot Wallet
                    '3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r',  # Bitstamp Cold Storage
                    '3DbAZpqKhUBu4rqafHzj7hWquoBL6gFBvj'   # Bitstamp-BTC-2
                ]
            },
            'bittrex': {
                'type': 'exchange',
                'addresses': [
                    '3KJrsjfg1dD6CrsTeHdM5SSk3PhXjNwhA7',  # Bittrex Hot Wallet
                    '3KJrsjfg1dD6CrsTeHdM5SSk3PhXjNwhA7',  # Bittrex Cold Storage
                    '3QW95MafxER9W7kWDcosQNdLk4Z36TYJZL'   # Bittrex-BTC-2
                ]
            },
            'kucoin': {
                'type': 'exchange',
                'addresses': [
                    '3M219KR5vEneNb47ewrPfWyb5jQ2DjxRP6',  # KuCoin Hot Wallet
                    '3H5JTt42K7RmZtromfTSefcMEFMMe18pMD',  # KuCoin Cold Storage
                    '3AfP9N7KNq2pYXiGQdgNJy8SD2Mo7pQKUR',  # KuCoin-BTC-2
                    'bc1qkucoinx89e7zk3m5jk4rt8h79x5znx89ppv3rq'  # KuCoin Operations
                ]
            },
            'gate_io': {
                'type': 'exchange',
                'addresses': [
                    '3FupZp77ySr7jwoLYEJ9mwzJpvoNBXsBnE',  # Gate.io Hot Wallet
                    '38WUPqGLXphpD1DwkMR8koGfd5UQfRnmrk',  # Gate.io Cold Storage
                ]
            },
            'ftx': {
                'type': 'exchange',
                'addresses': [
                    '3LQUu4v9z6KNch71j7kbj8GPeAGUo1FW6a',  # FTX Hot Wallet
                    '3E1jkR1PJ8hFUqCkDjimwPoF2bZVrkqnpv',  # FTX Cold Storage
                ]
            },
            'bybit': {
                'type': 'exchange',
                'addresses': [
                    '3JZq4atUahhuA9rLhXLMhhTo133J9rF97j',  # Bybit Hot Wallet
                    '3QW95MafxER9W7kWDcosQNdLk4Z36TYJZL',  # Bybit Cold Storage
                ]
            },
            'cryptocom': {
                'type': 'exchange',
                'addresses': [
                    '3P3QsMVK89JBNqZQv5zMAKG8FK3kJM4rjt',  # Crypto.com Hot Wallet
                    '3AAzK4Xbu8PTM8AD7gw2XaMZavL6xoKWHQ',  # Crypto.com Cold Storage
                ]
            },
            'okx': {
                'type': 'exchange',
                'addresses': [
                    'bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4',  # OKX Hot Wallet 1
                    'bc1qf2ep0kzskg2487v8mgwolg8dvmujpxrxhx6v5',  # OKX Hot Wallet 2
                    '3FpYfDGJSdkMAvZvCrwPHDqdmGqUkTsJys',          # OKX Cold Storage
                    'bc1q03xrw2lcd8nr8hzw0nv3phkz70t8hefc3k9sr0'   # OKX Deposit
                ]
            },
            'bitget': {
                'type': 'exchange',
                'addresses': [
                    'bc1qbitget89ppv3rqzk3m5jk4rt8h79x5znx45rt8h',  # Bitget Hot Wallet
                    '3BitgetXzwGYiGhuvZBd8HWNqKZ3YGhJbt',           # Bitget Cold Storage
                    'bc1qbitgetnx89e7zk3m5jk4rt8h79x5znx89ppv3r',   # Bitget Operations
                    '3BitgetDepositWalletXzwGYiGhuvZBd8HWNqKZ3'     # Bitget Deposit
                ]
            },
            'mexc': {
                'type': 'exchange',
                'addresses': [
                    'bc1qmexc89ppv3rqzk3m5jk4rt8h79x5znx45rt8h',  # MEXC Hot Wallet
                    '3MEXCXzwGYiGhuvZBd8HWNqKZ3YGhJbt',          # MEXC Cold Storage
                    'bc1qmexcnx89e7zk3m5jk4rt8h79x5znx89ppv3r'   # MEXC Operations
                ]
            },
            'whitebit': {
                'type': 'exchange',
                'addresses': [
                    '3WhiteBitExchangeHotWalletMainBTCxyz',
                    'bc1qwhitebit89e7zk3m5jk4rt8h79x5znx89ppv3r'
                ]
            },
            'bingx': {
                'type': 'exchange',
                'addresses': [
                    '3BingXMainWalletAddressHerePlease123',
                    'bc1qbingx89e7zk3m5jk4rt8h79x5znx89ppv3r'
                ]
            },
            'bitkub': {
                'type': 'exchange',
                'addresses': [
                    'bc1qbitkub89ppv3rqzk3m5jk4rt8h79x5znx45rt8h',
                    '3BitkubXzwGYiGhuvZBd8HWNqKZ3YGhJbt'
                ]
            },
            'hashkey': {
                'type': 'exchange',
                'addresses': [
                    'bc1qhashkey89e7zk3m5jk4rt8h79x5znx89ppv3r',
                    '3HashKeyExchangeWalletMainAddressxyz'
                ]
            },
            'bitmart': {
                'type': 'exchange',
                'addresses': [
                    '3BitMartMainWalletAddressHerePlease123',
                    'bc1qbitmart89e7zk3m5jk4rt8h79x5znx89ppv'
                ]
            },
            'lbank': {
                'type': 'exchange',
                'addresses': [
                    '3LBankExchangeMainWalletAddress123xyz',
                    'bc1qlbank89e7zk3m5jk4rt8h79x5znx89ppv3r'
                ]
            },
            'digifinex': {
                'type': 'exchange',
                'addresses': [
                    'bc1qdigifinex89ppv3rqzk3m5jk4rt8h79x5zn',
                    '3DigiFinexMainWalletAddressHerePlease'
                ]
            },
            'upbit': {
                'type': 'exchange',
                'addresses': [
                    '3UpbitMainExchangeWalletAddress123xyz',
                    'bc1qupbit89e7zk3m5jk4rt8h79x5znx89ppv3r'
                ]
            },
            'ascendex': {
                'type': 'exchange',
                'addresses': [
                    'bc1qascendex89ppv3rqzk3m5jk4rt8h79x5zn',
                    '3AscendEXMainWalletAddressHerePlease'
                ]
            },
            'bitrue': {
                'type': 'exchange',
                'addresses': [
                    '3BitrueMainExchangeWalletAddress123xyz',
                    'bc1qbitrue89e7zk3m5jk4rt8h79x5znx89ppv'
                ]
            },
            'dex_trade': {
                'type': 'exchange',
                'addresses': [
                    'bc1qdextrade89ppv3rqzk3m5jk4rt8h79x5zn',
                    '3DexTradeMainWalletAddressHerePlease'
                ]
            },
            'btse': {
                'type': 'exchange',
                'addresses': [
                    '3BTSEMainExchangeWalletAddress123xyz',
                    'bc1qbtse89e7zk3m5jk4rt8h79x5znx89ppv3r'
                ]
            },
            'bitmex': {
                'type': 'exchange',
                'addresses': [
                    '3BitMEXMainExchangeWalletAddress123xyz',
                    'bc1qbitmex89e7zk3m5jk4rt8h79x5znx89ppv'
                ]
            },
            'phemex': {
                'type': 'exchange',
                'addresses': [
                    'bc1qphemex89ppv3rqzk3m5jk4rt8h79x5znx4',
                    '3PhemexMainWalletAddressHerePlease123'
                ]
            },
            'bitflyer': {
                'type': 'exchange',
                'addresses': [
                    '3BitFlyerMainExchangeWalletAddress123',
                    'bc1qbitflyer89e7zk3m5jk4rt8h79x5znx89p'
                ]
            },
            'cexio': {
                'type': 'exchange',
                'addresses': [
                    'bc1qcexio89ppv3rqzk3m5jk4rt8h79x5znx45',
                    '3CEXIOMainWalletAddressHerePlease123'
                ]
            }
        }

        # Add mining pools
        self.known_addresses.update({
            'foundry_usa': {
                'type': 'mining_pool',
                'addresses': [
                    'bc1qx9t2l3pyny2spqpqlye8svce70nppwtaxwdrp4',
                    '3FrXk5rFBjVWvhEJF8tJ5nPYpr2LVWBCqD'
                ]
            },
            'antpool': {
                'type': 'mining_pool',
                'addresses': [
                    'bc1qd8fp5hc7rs620y4vxxn5vármegy66kpy8hau9at',
                    '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
                ]
            },
            'f2pool': {
                'type': 'mining_pool',
                'addresses': [
                    'bc1qtw30nantkrh7y5ue73gm4mj4tdeqxwz8z8s626',
                    '3ChzgHhBqR1Y5LkcJQHYmUFfuGekkH55UD'
                ]
            },
            'binance_pool': {
                'type': 'mining_pool',
                'addresses': [
                    'bc1qxaq9ya4903w2ene5z8lmjmgvz9rxy84dl0j2h2',
                    '34Jpa4Eu3ApoPVUKNTN2WsuiNP5JXqpJo6'
                ]
            },
            'btccom': {
                'type': 'mining_pool',
                'addresses': [
                    'bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4',
                    '3KJrsjfg1dD6CrsTeHdM5SSk3PhXjNwhA7'
                ]
            }
        })

        # Add Crypto.com expanded addresses
        self.known_addresses['cryptocom'].update({
            'type': 'exchange',
            'addresses': [
                'bc1q9d4ywgfnd8h43da5tpcxcn6ajv590cg6d3tg6axemvljvt2k76zs4s0llh',  # Main wallet
                '3QF8LBkqHwKHhVFpgCZg7ssJDiXXYysHUP',  # Hot wallet
                'bc1qk9y7qz7d984syxr2z7gqkcf0tqwrhx5t5sd870',  # Cold storage
                '3D8qAoMkZ8F1YGzqpJU5Z7cJpPZfhUDxhu',  # Exchange wallet
                '3PxqibGtHR9Ymh1GJvyVLnVh94G5qcUxMP'   # Institutional
            ]
        })

        # Add important Bitcoin trading companies
        self.known_addresses.update({
            'microstrategy': {
                'type': 'corporate',
                'addresses': [
                    'bc1qazcm763858nkj2dj986etajv6wquslv8uxwczt',  # Main treasury
                    'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',  # Secondary
                    '1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ'           # Corporate
                ]
            },
            'tesla': {
                'type': 'corporate',
                'addresses': [
                    'bc1q4c8c0hx8qps3mpk3zqguwwd6glq6p5h8z5rk9q',
                    '1HrZxE4SqgZAYGzRqw8qVvora3qnJvWTWR'
                ]
            },
            'square': {
                'type': 'corporate',
                'addresses': [
                    'bc1pw508d6qejxtdg4y5r3zarvary0c5xw7kw508d6',
                    '3E1ZxHvZL4SmQxGNQgYzFHUK1N8AQ3HJnE'
                ]
            },
            'grayscale': {
                'type': 'investment',
                'addresses': [
                    'bc1qe7nps5yv7ruc884zscwrk9g2mxvqh7tkxfxwny',
                    'bc1qkz7u6l5c8wqz8nc5yxkls2j8u4y2hkdzlgfnl4',
                    '3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r'
                ]
            }
        })

        # Enhanced exchange identification patterns
        self.exchange_identifiers = {
            'binance': {
                'prefixes': ['3FaA', '1ND', '34xp', '1LQv', 'bnb1', 'bc1q'],
                'patterns': [
                    r'^(3FaA4dJuuvJFyUHbqHLkZKJcuDPugvG3zE)',  # Hot Wallet
                    r'^(1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s)',  # Cold Storage
                    r'^(34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo)',  # Reserve
                    r'binance|bnb|binancebtc'
                ],
                'type': 'exchange'
            },
            'coinbase': {
                'prefixes': ['3Kzh', '1CWY', '1FxK', '1GR9', 'bc1q'],
                'patterns': [
                    r'^(3FzScn724foqFRWvL1kCZwitQvcxrnSQ4K)',  # Hot Wallet
                    r'^(3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS)',  # Cold Storage
                    r'^(1CWYTCvwKfH5cWnX3VcAykgTsmjsuB3wXe)',  # Prime
                    r'coinbase|cb_'
                ],
                'type': 'exchange'
            },
            'crypto_com': {
                'prefixes': ['bc1q9d', '3QF8', 'bc1qk', '3D8q', '3Pxq'],
                'patterns': [
                    r'^(bc1q9d4ywgfnd8h43da5tpcxcn6ajv590cg6d3tg6axemvljvt2k76zs4s0llh)',  # Main
                    r'^(3QF8LBkqHwKHhVFpgCZg7ssJDiXXYysHUP)',  # Hot
                    r'^(bc1qk9y7qz7d984syxr2z7gqkcf0tqwrhx5t5sd870)',  # Cold
                    r'cryptocom|cro'
                ],
                'type': 'exchange'
            },
            'kraken': {
                'prefixes': ['3FupZ', '3H5J', '3AfP', '3E1j'],
                'patterns': [
                    r'^(3FupZp77ySr7jwoLYEJ9mwzJpvoNBXsBnE)',  # Hot Wallet
                    r'^(3H5JTt42K7RmZtromfTSefcMEFMMe18pMD)',  # Cold Storage
                    r'kraken'
                ],
                'type': 'exchange'
            },
            'bybit': {
                'prefixes': ['3JZq', '3QW9'],
                'patterns': [
                    r'^(3JZq4atUahhuA9rLhXLMhhTo133J9rF97j)',  # Hot
                    r'^(3QW95MafxER9W7kWDcosQNdLk4Z36TYJZL)',  # Cold
                    r'bybit'
                ],
                'type': 'exchange'
            },
            'okx': {
                'prefixes': ['bc1q', '3Fp', 'bc1q0'],
                'patterns': [
                    r'^(bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4)',  # Hot 1
                    r'^(3FpYfDGJSdkMAvZvCrwPHDqdmGqUkTsJys)',  # Cold
                    r'okx|okex'
                ],
                'type': 'exchange'
            }
        }

    def get_latest_block(self):
        """Get the latest block hash and ensure we don't process duplicates"""
        try:
            response = requests.get(f"{self.base_url}/latestblock")
            block_data = response.json()
            current_height = block_data['height']
            current_hash = block_data['hash']
            
            # If this is our first block, initialize
            if self.last_block_height is None:
                self.last_block_height = current_height
                return current_hash
                
            # If we've seen this block already, return None
            if current_hash in self.processed_blocks:
                return None
                
             # If this is a new block
            if current_height > self.last_block_height:
                self.last_block_height = current_height
                # Keep track of last 1000 blocks to manage memory
                if len(self.processed_blocks) > 1000:
                    self.processed_blocks.clear()
                self.processed_blocks.add(current_hash)
                print(f"\nNew Block: {current_height} | Hash: {current_hash[:8]}...")
                return current_hash
                
            return None
            
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

    def get_address_label(self, address):
        """Get the entity label for an address"""
        for entity, info in self.known_addresses.items():
            if address in info['addresses']:
                return f"({entity.upper()} {info['type']})"
        return ""

    def update_address_stats(self, address, is_sender, btc_amount, timestamp):
        """Update statistics for an address"""
        stats = self.address_stats[address]
        if is_sender:
            stats['sent_count'] += 1
            stats['total_sent'] += btc_amount
        else:
            stats['received_count'] += 1
            stats['total_received'] += btc_amount
        stats['last_seen'] = timestamp

    def get_address_summary(self, address):
        """Get formatted summary of address activity"""
        stats = self.address_stats[address]
        entity_label = self.get_address_label(address)
        return (f"{entity_label} "
                f"[↑{stats['sent_count']}|↓{stats['received_count']}] "
                f"Total: ↑{stats['total_sent']:.2f}|↓{stats['total_received']:.2f} BTC")

    def identify_address(self, address):
        """Enhanced address identification with improved exchange detection"""
        if not address:
            return None
            
        address = str(address).lower().strip()
        
        # Check known exchanges first
        for exchange, info in self.exchange_identifiers.items():
            # Check prefixes
            if any(address.startswith(prefix.lower()) for prefix in info['prefixes']):
                return {
                    'name': exchange,
                    'type': info['type'],
                    'confidence': 'high',
                    'address': address
                }
            
            # Check patterns
            if any(re.search(pattern, address, re.IGNORECASE) for pattern in info['patterns']):
                return {
                    'name': exchange,
                    'type': info['type'],
                    'confidence': 'high',
                    'address': address
                }
        
        # Fall back to existing checks
        return self._fallback_address_check(address)

    def determine_transaction_type(self, sender, receiver):
        """Enhanced transaction type determination including stablecoin mints/burns"""
        
        # Check for stablecoin mint/burn
        for stablecoin, addresses in self.stablecoin_addresses.items():
            # Check for mint
            if sender == addresses['mint_address']:
                return {
                    'type': f'{stablecoin.upper()}_MINT',
                    'from_entity': {'name': f'{stablecoin}_mint', 'type': 'stablecoin'},
                    'to_entity': self.identify_address(receiver)
                }
            # Check for burn
            elif receiver == addresses['burn_address']:
                return {
                    'type': f'{stablecoin.upper()}_BURN',
                    'from_entity': self.identify_address(sender),
                    'to_entity': {'name': f'{stablecoin}_burn', 'type': 'stablecoin'}
                }
            # Check for treasury movement
            elif sender == addresses['treasury'] or receiver == addresses['treasury']:
                return {
                    'type': f'{stablecoin.upper()}_TREASURY',
                    'from_entity': self.identify_address(sender),
                    'to_entity': self.identify_address(receiver)
                }

        # Continue with existing checks
        sender_info = self.identify_address(sender)
        receiver_info = self.identify_address(receiver)
        
        if sender_info and receiver_info:
            return {
                'type': 'INTERNAL TRANSFER',
                'from_entity': sender_info,
                'to_entity': receiver_info
            }
        elif sender_info:
            return {
                'type': 'WITHDRAWAL',
                'from_entity': sender_info,
                'to_entity': None
            }
        elif receiver_info:
            return {
                'type': 'DEPOSIT',
                'from_entity': None,
                'to_entity': receiver_info
            }
        else:
            return {
                'type': 'unknown transfer',
                'from_entity': None,
                'to_entity': None
            }

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
        
        timestamp = datetime.fromtimestamp(tx.get('time', 0))
        
        # Update address statistics
        self.update_address_stats(sender, True, btc_value, timestamp)
        self.update_address_stats(receiver, False, btc_value, timestamp)
        
        # Get transaction type and entities involved
        tx_info = self.determine_transaction_type(sender, receiver)
        
        # Calculate fee
        output_value = sum(out.get('value', 0) for out in tx.get('out', []))
        fee = (input_value - output_value) / self.satoshi_to_btc
        
        return {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'transaction_hash': tx.get('hash', 'Unknown'),
            'sender': sender,
            'receiver': receiver,
            'btc_volume': round(btc_value, 4),
            'fee_btc': round(fee, 8),
            'tx_type': tx_info['type'],
            'from_entity': tx_info['from_entity'],
            'to_entity': tx_info['to_entity']
        }

    def print_transaction(self, tx):
        """Format transaction alerts with clean exchange detection"""
        # Determine emoji based on type and amount
        tx_type = tx['tx_type'].lower()
        btc_amount = tx['btc_volume']
        
        # Enhanced emoji selection
        if '_mint' in tx_type:
            emoji = "💵"
        elif '_burn' in tx_type:
            emoji = "🔥"
        elif '_treasury' in tx_type:
            emoji = "🏦"
        elif 'exchange' in tx_type or any(ex in tx_type for ex in ['coinbase', 'gemini', 'bybit', 'binance']):
            emoji = "💱" * min(3, max(1, int(btc_amount / 500)))
        else:
            emoji_count = min(8, max(1, int(btc_amount / 500)))
            emoji = "🚨" * emoji_count

        # Format amounts with commas
        btc_formatted = f"{btc_amount:,.0f}"
        usd_value = btc_amount * 96073.862
        usd_formatted = f"{usd_value:,.0f}"
        
        # Format fee
        fee_sats = tx['fee_btc'] * 100000000
        fee_usd = tx['fee_btc'] * 96073.862
        
        # Get entity names (lowercase)
        from_entity = tx['from_entity']['name'].lower() if tx['from_entity'] else "unknown"
        to_entity = tx['to_entity']['name'].lower() if tx['to_entity'] else "unknown"
        
        # List of major exchanges to track
        exchanges = ['coinbase', 'gemini', 'bybit', 'binance', 'kraken', 'bitfinex', 'okx', 'htx']
        
        # Format transaction type
        clean_type = tx_type.replace('_', ' ').lower()
        
        # Base message
        message = (
            f"{emoji} {btc_formatted} #btc ({usd_formatted} USD) transferred "
            f"({clean_type}) from #{from_entity} to #{to_entity} "
            f"for {fee_sats:.2f} sats (${fee_usd:.0f}) fees"
        )
        
        # Add exchange transfer prefix if applicable
        if any(ex in from_entity or ex in to_entity for ex in exchanges):
            message = "💱 Exchange Transfer Alert:\n" + message
        
        # Add mega whale prefix for very large transactions
        if btc_amount > 1000:
            message = "𓆟  alert shark 𓆞\n" + message
        
        print(message)
        return message

    def monitor_transactions(self):
        """Main method to track whale transactions"""
        print(f"Tracking Bitcoin transactions over {self.min_btc} BTC...")
        print("Waiting for new blocks...")
        
        while True:
            try:
                block_hash = self.get_latest_block()
                
                if block_hash:
                    transactions = self.get_block_transactions(block_hash)
                    processed_count = 0
                    whale_count = 0
                    
                    for tx in transactions:
                        processed_count += 1
                        whale_tx = self.process_transaction(tx)
                        if whale_tx:
                            whale_count += 1
                            self.print_transaction(whale_tx)
                    
                    print(f"Processed {processed_count} transactions, found {whale_count} whale movements")
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(30)

    def is_exchange_address(self, address_info):
        """Improved exchange detection"""
        if not address_info:
            return False
        
        address_str = str(address_info).lower()
        for exchange, patterns in self.exchange_patterns.items():
            if any(pattern in address_str for pattern in patterns):
                return exchange
        return False

if __name__ == "__main__":
    tracker = BitcoinWhaleTracker(min_btc=1000)  # Changed from 500 to 1000
    tracker.monitor_transactions()  # Changed from track_whale_transactions to monitor_transactions