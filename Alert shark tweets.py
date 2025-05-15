import time
import tweepy
import logging
from alert_pricebar import test_display as btc_price_display
from eth_pricebar import test_display as eth_price_display
from btc_monitor import BitcoinWhaleTracker  # Fixed import path
from keys import bearer_token, consumer_key, consumer_secret, access_token, access_token_secret
import re

class TwitterBot:
    def __init__(self):
        # Use Twitter API v2 authentication
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )
        
        # Test authentication
        try:
            me = self.client.get_me()
            print(f"Authentication OK - User ID: {me.data.id}")
        except Exception as e:
            print("Error during authentication:", str(e))
            raise
            
        self.whale_tracker = BitcoinWhaleTracker(min_btc=1000)  # Changed to 1000 BTC minimum
        
        # Updated known exchange names to match btc_monitor.py
        self.known_exchanges = [
            'binance', 'coinbase', 'kraken', 'bitfinex',
            'gemini', 'bybit', 'kucoin', 'huobi',
            'okex', 'ftx', 'gate.io'
        ]
        
        # Add high-risk entity tracking
        self.high_risk_entities = [
            'lazarus_group',
            'exchangex',
            'stolen_funds',
            'silk_road'  # Added Silk Road identifier
        ]
        
        # Add known Silk Road wallets
        self.silk_road_wallets = [
            '1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX',  # Known Silk Road wallet
            'bc1qa5wkgaew2dkv56kfvj49j0av5nml45x9ek9hz6',  # Associated wallet
            '1HQ3Go3ggs8pFnXuHVHRytPCq5fGG8Hbhx'  # Historical Silk Road wallet
        ]
        
        # Add priority alert thresholds
        self.alert_thresholds = {
            'normal': 1000,      # Regular whale transfers
            'high_risk': 100,    # Suspicious transfers
            'silk_road': 10      # Extra sensitive threshold for Silk Road wallets
        }
        
        # Add timeout settings
        self.timeouts = {
            'btc_monitor': 30,  # Maximum seconds to wait for BTC monitor
            'price_update': 15,  # Maximum seconds to wait for price updates
            'tweet_delay': 60    # Delay between tweets
        }
        
        # Track last update times
        self.last_updates = {
            'btc_price': 0,
            'eth_price': 0,
            'whale_alert': 0
        }
        
        # Update timing configurations
        self.post_intervals = {
            'btc_price': 900,    # 15 minutes
            'eth_price': 900,    # 15 minutes
            'whale_alert': 300   # 5 minutes
        }
        
        self.wait_times = {
            'after_btc_price': 120,  # 2 minutes
            'after_eth_price': 180,  # 3 minutes
            'between_alerts': 30      # 30 seconds between whale alerts
        }
        
        # Enhanced exchange patterns and addresses
        self.exchange_patterns = {
            'binance': {
                'addresses': [
                    '34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo',  # Binance Cold Wallet
                    '3FaA4dJuuvJFyUHbqHLkZKJcuDPugvG3zE',  # Binance Hot Wallet 1
                    '1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s',  # Binance Hot Wallet 2
                    'bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h'  # Binance-BTC
                ],
                'patterns': [r'binance', r'bnb', r'binancebtc', r'^3FaA', r'^1ND']
            },
            'coinbase': {
                'addresses': [
                    '3FzScn724foqFRWvL1kCZwitQvcxrnSQ4K',  # Coinbase Main
                    '3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS',  # Coinbase Cold
                    '1CWYTCvwKfH5cWnX3VcAykgTsmjsuB3wXe',  # Coinbase Hot
                    'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'  # Coinbase Prime
                ],
                'patterns': [r'coinbase', r'cb_', r'^3Kzh', r'^1CWY']
            },
            'kraken': {
                'addresses': [
                    '3FupZp77ySr7jwoLYEJ9mwzJpvoNBXsBnE',  # Kraken Main
                    '3H5JTt42K7RmZtromfTSefcMEFMMe18pMD',  # Kraken Storage
                    'bc1qsp7q8z5c7dqx0m9xte7jeexcwqgtwjqz7te47n'  # Kraken New
                ],
                'patterns': [r'kraken', r'^3FupZ', r'^3H5J']
            },
            'okx': {
                'addresses': [
                    'bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4',  # OKX Main
                    '3LQUu4v9z6KNch71j7kbj8GPeAGUo1FW6a',  # OKX Hot
                    '3FpYfDGJSdkMAvZvCrwPHDqdmGqUkTsJys'   # OKX Cold
                ],
                'patterns': [r'okx', r'okex', r'^3LQU']
            },
            'bitget': {
                'addresses': [
                    'bc1qbitget89ppv3rqzk3m5jk4rt8h79x5znx45rt8h',
                    '3BitgetXzwGYiGhuvZBd8HWNqKZ3YGhJbt'
                ],
                'patterns': [r'bitget', r'^3Bitget']
            },
            'wintermute': {
                'addresses': [
                    'bc1q0f3gdx3al9nxkw9m4x96qvr4j5dmgpx9v0r5g5',  # Wintermute Main
                    '3WintermuteTradingWalletMainBTCxyz'
                ],
                'patterns': [r'wintermute', r'^3Winter']
            },
            'gemini': {
                'addresses': [
                    '3P3QsMVK89JBNqZQv5zMAKG8FK3kJM4rjt',  # Gemini Main
                    '393HLwqnkrJMxYQTHjWBJPAKC3UG6k6FwB',  # Gemini Hot
                    'bc1qgemini89ppv3rqzk3m5jk4rt8h79x5znx45'
                ],
                'patterns': [r'gemini', r'^3P3Q', r'^393H']
            }
        }

        # Enhanced exchange detection with more patterns and addresses
        self.exchange_identifiers = {
            'binance': {
                'prefixes': ['3FaA', '1ND', '34xp', '1LQv', 'bnb1', 'bc1q'],
                'patterns': [
                    r'^(3FaA4dJuuvJFyUHbqHLkZKJcuDPugvG3zE)',  # Hot Wallet
                    r'^(1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s)',  # Cold Storage
                    r'binance|bnb|binancebtc'
                ],
                'type': 'tier1_exchange'
            },
            'binance_us': {
                'prefixes': ['3BUS', 'bc1q', '1BUS'],
                'patterns': [r'binanceus|bus_'],
                'type': 'regional_exchange'
            },
            'okx': {
                'prefixes': ['bc1q', '3Fp', 'bc1q0'],
                'patterns': [
                    r'^(bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4)',
                    r'^(3FpYfDGJSdkMAvZvCrwPHDqdmGqUkTsJys)',
                    r'okx|okex'
                ],
                'type': 'tier1_exchange'
            },
            'cryptocom': {
                'prefixes': ['bc1q9d', '3QF8', 'bc1qk', '3D8q'],
                'patterns': [
                    r'^(bc1q9d4ywgfnd8h43da5tpcxcn6ajv590cg6d3tg6axemvljvt2k76zs4s0llh)',
                    r'crypto\.?com|cro'
                ],
                'type': 'tier1_exchange'
            },
            'kraken': {
                'prefixes': ['3FupZ', '3H5J', '3AfP', '3E1j'],
                'patterns': [
                    r'^(3FupZp77ySr7jwoLYEJ9mwzJpvoNBXsBnE)',
                    r'^(3H5JTt42K7RmZtromfTSefcMEFMMe18pMD)',
                    r'kraken'
                ],
                'type': 'tier1_exchange'
            },
            'bybit': {
                'prefixes': ['3JZq', '3QW9', 'bc1qbyb'],
                'patterns': [
                    r'^(3JZq4atUahhuA9rLhXLMhhTo133J9rF97j)',
                    r'bybit'
                ],
                'type': 'tier1_exchange'
            },
            'kucoin': {
                'prefixes': ['bc1qkuc', '3Kuc'],
                'patterns': [r'kucoin'],
                'type': 'tier2_exchange'
            },
            'gateio': {
                'prefixes': ['3GATE', 'bc1qgt'],
                'patterns': [r'gate\.?io'],
                'type': 'tier2_exchange'
            },
            'htx': {  # Former Huobi
                'prefixes': ['3HTX', 'bc1qh'],
                'patterns': [r'htx|huobi'],
                'type': 'tier2_exchange'
            },
            'bitfinex': {
                'prefixes': ['3D2o', '3JZq', '3QW9'],
                'patterns': [r'bitfinex|bfx'],
                'type': 'tier1_exchange'
            },
            'mexc': {
                'prefixes': ['3MEXC', 'bc1qm'],
                'patterns': [r'mexc'],
                'type': 'tier2_exchange'
            },
            'bitmex': {
                'prefixes': ['3BMEX', 'bc1qbm'],
                'patterns': [r'bitmex'],
                'type': 'derivatives_exchange'
            },
            'bitget': {
                'prefixes': ['3BG', 'bc1qbg'],
                'patterns': [r'bitget'],
                'type': 'tier2_exchange'
            },
            'whitebit': {
                'prefixes': ['3WB', 'bc1qwb'],
                'patterns': [r'whitebit'],
                'type': 'tier2_exchange'
            },
            'bitmart': {
                'prefixes': ['3BMT', 'bc1qbm'],
                'patterns': [
                    r'^(bc1qbitmart[a-zA-Z0-9]{30,})',
                    r'bitmart'
                ],
                'type': 'tier3_exchange'
            },
            'lbank': {
                'prefixes': ['3LBK', 'bc1ql'],
                'patterns': [
                    r'^(bc1qlbank[a-zA-Z0-9]{30,})',
                    r'lbank'
                ],
                'type': 'tier3_exchange'
            },
            'bitstamp': {
                'prefixes': ['3BiS', 'bc1qbs'],
                'patterns': [
                    r'^(3BitstampBTCWallet[a-zA-Z0-9]{20,})',
                    r'bitstamp'
                ],
                'type': 'tier1_exchange'
            },
            'bitflyer': {
                'prefixes': ['3BFJ', 'bc1qbf'],
                'patterns': [
                    r'^(bc1qbitflyer[a-zA-Z0-9]{30,})',
                    r'bitflyer'
                ],
                'type': 'regional_asian'
            },
            'bithumb': {
                'prefixes': ['3BTH', 'bc1qbh'],
                'patterns': [
                    r'^(3BithumbMainWallet[a-zA-Z0-9]{20,})',
                    r'bithumb'
                ],
                'type': 'regional_asian'
            },
            'upbit': {
                'prefixes': ['3UPB', 'bc1qup'],
                'patterns': [
                    r'^(bc1qupbit[a-zA-Z0-9]{30,})',
                    r'upbit'
                ],
                'type': 'regional_asian'
            },
            'bitbank': {
                'prefixes': ['3BBK', 'bc1qbb'],
                'patterns': [
                    r'^(bc1qbitbank[a-zA-Z0-9]{30,})',
                    r'bitbank'
                ],
                'type': 'tier3_exchange'
            },
            'ascendex': {
                'prefixes': ['3ASC', 'bc1qa'],
                'patterns': [
                    r'^(bc1qascendex[a-zA-Z0-9]{30,})',
                    r'ascendex|bitmax'
                ],
                'type': 'tier3_exchange'
            },
            'coinex': {
                'prefixes': ['3CEX', 'bc1qcx'],
                'patterns': [
                    r'^(bc1qcoinex[a-zA-Z0-9]{30,})',
                    r'coinex'
                ],
                'type': 'tier3_exchange'
            },
            'bitvavo': {
                'prefixes': ['3BVV', 'bc1qbv'],
                'patterns': [
                    r'^(bc1qbitvavo[a-zA-Z0-9]{30,})',
                    r'bitvavo'
                ],
                'type': 'regional_european'
            },
            'phemex': {
                'prefixes': ['3PHX', 'bc1qph'],
                'patterns': [
                    r'^(bc1qphemex[a-zA-Z0-9]{30,})',
                    r'phemex'
                ],
                'type': 'derivatives_exchange'
            }
        }

        # Add exchange tiers for better classification
        self.exchange_tiers = {
            'tier1_exchange': ['binance', 'coinbase', 'kraken', 'okx', 'bybit', 'bitfinex', 'cryptocom'],
            'tier2_exchange': ['kucoin', 'gateio', 'htx', 'mexc', 'bitget', 'whitebit'],
            'derivatives_exchange': ['bitmex', 'deribit', 'bybit_derivatives'],
            'regional_exchange': ['binance_us', 'bitkub', 'upbit', 'bitflyer'],
            'tier3_exchange': [
                'bitmart', 'lbank', 'digifinex', 'upbit', 'xt_com',
                'ascendex', 'bitrue', 'coinex', 'dex_trade', 'btse',
                'bitstamp', 'bitbank', 'indodax', 'bitso', 'bithumb',
                'bitvavo', 'phemex', 'bitflyer', 'exmo'
            ],
            'regional_asian': [
                'coinw', 'bithumb', 'upbit', 'bitflyer', 'gmo_japan',
                'coinone', 'zaif', 'btcbox', 'bibox', 'wazirx'
            ],
            'regional_european': [
                'bitvavo', 'bitpanda', 'paymium', 'coinmetro',
                'btcturk', 'cex_io', 'bitexen', 'kuna'
            ],
            'regional_latam': [
                'bitso', 'mercado_bitcoin', 'foxbit', 'novadax',
                'bitrue_latam', 'toctoc'
            ],
            'dex_platform': [
                'dex_trade', 'latoken', 'probit', 'nominex',
                'changelly_pro', 'bitexbook'
            ]
        }

        # Add address patterns for regional exchanges
        self.regional_patterns = {
            'asian': [r'bithumb', r'upbit', r'bitflyer', r'coinone', r'zaif'],
            'european': [r'bitvavo', r'btcturk', r'cex\.io', r'paymium'],
            'latam': [r'bitso', r'mercado', r'foxbit', r'novadax'],
            'african': [r'valr', r'chainex', r'altcointrader']
        }

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('TwitterBot')

    def post_tweet(self, message):
        try:
            # Use v2 create_tweet instead of update_status
            tweet = self.client.create_tweet(text=message)
            self.logger.info(f"Tweet posted successfully with id: {tweet.data['id']}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to tweet: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error in price update: {e}")
            return None

    def identify_exchange(self, address):
        """Enhanced exchange identification with tiered classification"""
        if not address:
            return None
            
        address = str(address).lower().strip()
        
        # Direct address match
        for exchange, info in self.exchange_identifiers.items():
            # Check exact addresses if available
            if 'addresses' in info and address in [addr.lower() for addr in info['addresses']]:
                return {
                    'name': exchange,
                    'type': info['type'],
                    'confidence': 'high',
                    'tier': self._get_exchange_tier(exchange)
                }
            
            # Check prefixes
            if any(address.startswith(prefix.lower()) for prefix in info['prefixes']):
                return {
                    'name': exchange,
                    'type': info['type'],
                    'confidence': 'medium',
                    'tier': self._get_exchange_tier(exchange)
                }
            
            # Check patterns
            if any(re.search(pattern, address, re.IGNORECASE) for pattern in info['patterns']):
                return {
                    'name': exchange,
                    'type': info['type'],
                    'confidence': 'medium',
                    'tier': self._get_exchange_tier(exchange)
                }
        
        return {
            'name': 'unknown',
            'type': 'unknown',
            'confidence': 'low',
            'tier': 'unknown'
        }

    def identify_regional_exchange(self, address):
        """Identify regional exchanges"""
        address = str(address).lower().strip()
        
        for region, patterns in self.regional_patterns.items():
            if any(re.search(pattern, address, re.IGNORECASE) for pattern in patterns):
                return {
                    'name': 'regional_exchange',
                    'region': region,
                    'confidence': 'medium'
                }
        return None

    def _get_exchange_tier(self, exchange_name):
        """Helper method to get exchange tier"""
        for tier, exchanges in self.exchange_tiers.items():
            if exchange_name in exchanges:
                return tier
        return 'unknown'

    def format_exchange_alert(self, alert, from_exchange, to_exchange):
        """Format alert based on exchange identification"""
        formatted_alert = f"🚨 Whale Alert 🚨\n"
        formatted_alert += f"Transaction detected:\n"
        formatted_alert += f"From: {from_exchange['name']} ({from_exchange['confidence']} confidence)\n"
        formatted_alert += f"To: {to_exchange['name']} ({to_exchange['confidence']} confidence)\n"
        formatted_alert += f"Details: {alert}\n"
        return formatted_alert

    def check_whale_alert(self):
        """Enhanced whale alert checking"""
        try:
            alerts = self.whale_tracker.monitor_transactions()
            
            if alerts:
                for alert in alerts:
                    # Identify exchanges in the transaction
                    from_exchange = self.identify_exchange(alert.get('from_address', ''))
                    to_exchange = self.identify_exchange(alert.get('to_address', ''))
                    
                    # Format alert based on exchange identification
                    if from_exchange['confidence'] != 'low' or to_exchange['confidence'] != 'low':
                        alert = self.format_exchange_alert(alert, from_exchange, to_exchange)
                    
                    if self.post_tweet(alert):
                        self.logger.info(f"Posted whale alert: {alert[:50]}...")
                        time.sleep(self.wait_times['between_alerts'])
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in whale alert: {e}")
            return False

    def check_eth_price(self):
        """Run and post ETH price status"""
        try:
            eth_status = eth_price_display()
            if eth_status:
                self.logger.info("ETH price status generated")
                if self.post_tweet(eth_status):
                    self.logger.info("Posted ETH price update successfully")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error in ETH price update: {e}")
            return False

    def run(self):
        """Main loop with specified sequence and timing"""
        self.logger.info("Starting Twitter Bot...")
        
        while True:
            try:
                current_time = time.time()
                
                # 1. First check BTC price from alert_pricebar.py
                if current_time - self.last_updates['btc_price'] >= self.post_intervals['btc_price']:
                    self.logger.info("Step 1: Checking BTC price from alert_pricebar.py...")
                    btc_status = btc_price_display()
                    if btc_status and self.post_tweet(btc_status):
                        self.last_updates['btc_price'] = current_time
                        self.logger.info("BTC price posted, waiting 2 minutes...")
                        time.sleep(self.wait_times['after_btc_price'])
                
                # 2. Then check ETH price after 2 minutes
                if current_time - self.last_updates['eth_price'] >= self.post_intervals['eth_price']:
                    self.logger.info("Step 2: Checking ETH price...")
                    if self.check_eth_price():
                        self.last_updates['eth_price'] = current_time
                        self.logger.info("ETH price posted, waiting 3 minutes...")
                        time.sleep(self.wait_times['after_eth_price'])
                
                # 3. Finally check BTC monitor after 3 minutes
                if current_time - self.last_updates['whale_alert'] >= self.post_intervals['whale_alert']:
                    self.logger.info("Step 3: Checking BTC monitor...")
                    if self.check_whale_alert():
                        self.last_updates['whale_alert'] = current_time
                        time.sleep(self.wait_times['between_alerts'])
                
                # Small delay before next cycle
                time.sleep(15)
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.logger.info("Waiting 30 seconds before retry...")
                time.sleep(30)

if __name__ == "__main__":
    bot = TwitterBot()
    bot.run()