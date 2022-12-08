import time
import datetime
from time import sleep


from tweepy import auth


def btc():
    url = "https://api.coinbase.com/v2/prices/spot?currency=USD"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    amount_data = parsed["data"]["amount"]
    bitcoin = float(amount_data)
    return bitcoin

def eth():
    url = "https://api.coinbase.com/v2/prices/ETH-USD/spot"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    amount_data = parsed["data"]["amount"]
    eth_price = float(amount_data)
    return eth_price

bit_2017 = 100000.1 #19783.21
bit_current = float(btc())
num= bit_current/bit_2017*100

def price_data():
    ratio = eth()/btc()
    ratioD = ("{0:.2f}".format(ratio))
    return ratioD 

"""this would print out the value of the current bitcion price"""
def checkpercent():
 if num <= 25 :
  return '₿itcoin   ▼ \n\n'
 elif num >= 25 : 
  return  '₿itcoin  ▲\n\n' 
 elif num == 50 : 
  return '₿itcoin  ∞ \n\n'
 elif num >=50 :
  return  '₿itcoin ▲ \n\n'

"""this is to printout the first part of the tweet, the top half""" 
    
def bitcoinData ():
 if num <= 0 :
    return ("⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%")
 elif num <= 1 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 1%")
 elif num <= 2 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 2%")
 elif num <= 3 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 3%")
 elif num <= 4 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 4%")
 elif num <= 5 :
   return  ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 5%")
 elif num <= 6 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 6%")
 elif num <= 7 : 
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 7%")
 elif num <= 8 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 8%")
 elif num <= 9 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 9%")
 elif num <= 10 : 
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 10%")
 elif num <= 11 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 11%")
 elif num <= 12 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜12%")
 elif num <= 13 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 13%")
 elif num <= 14 : 
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 14%")
 elif num <= 15 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜15%")
 elif num <= 16 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 16%")
 elif num <= 17 : 
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 17%")
 elif num <= 18 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 18%")
 elif num <= 19 : 
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 19%")
 elif num <= 20 :
    return ("⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜ 20%")
 elif num <= 21 :
    return ("⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜  21%")
 elif num <= 22 :
    return ("⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜  22%")
 elif num <= 23 :
    return ("⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜  23%")
 elif num <= 24 :
    return ("⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜  24%")
 elif num <= 25 :
    return ("⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜ 25%")
 elif num <= 26 :
    return("⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜  26%") 
 elif num <= 27 :
    return ("⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜ 27%")
 elif num <= 28 :
   return ("⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜  28%")
 elif num <= 29 :
    return ("⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜  29%")
 elif num <= 30 :
    return ("⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜ 30%")
 elif num <= 31 :
    return ("⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜ 31%")
 elif num <= 32 :
    return ("⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜ 32%")
 elif num <= 33 :
    return ("⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜ 33%")
 elif num <= 34 :
    return ("⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜ 34%") 
 elif num <= 35 :
    return ("⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜ 35%")
 elif num <= 36 :
    return ("⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜ 36%")
 elif num <= 37 :
    return ("⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜ 37%")
 elif num <= 38 :
    return ("⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜ 38%")
 elif num <= 39 :
    return ("⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜39%")
 elif num <= 40 :
    return ("⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜40%")
 elif num <= 41 :
    return ("⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜ 41%")
 elif num <= 42 :
    return ("⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜ 42%")
 elif num <= 43 :
    return ("⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜ 43%")
 elif num <= 44 :
    return ("⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜44%")
 elif num <= 45 : 
    return ("⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜45%") 
 elif num <= 46  : 
    return ("⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜46%") 
 elif num <= 47  : 
    return ("⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜ 47%") 
 elif num <= 48 : 
    return ("⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜48%")
 elif num <= 49 : 
    return ("⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜ 49%") 
 elif num <= 50 : 
    return ("⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜ 50%") 
 elif num <= 51 : 
    return ("⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜ 51%") 
 elif num <= 52 : 
    return ("⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜ 52%") 
 elif num <= 53 : 
    return ("⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜53%") 
 elif num <= 54 : 
    return ("⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜ 54%") 
 elif num <= 55 : 
    return ("⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜ 55%") 
 elif num <= 56 : 
    return ("⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜ 56%") 
 elif num <= 57 : 
    return ("⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜ 57%")
 elif num <= 58 : 
    return ("⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜ 58%")
 elif num <= 59 : 
    return ("⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜ 59%")
 elif num <= 60 : 
    return ("⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜  60%")
 elif num <= 61 : 
    return ("⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜  61%")
 elif num <= 62 : 
    return ("⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜  62%")
 elif num <= 63 : 
    return ("⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜  63%") 
 elif num <= 64 : 
    return ("⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜  64%")
 elif num <= 65 : 
    return ("⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜  65%")
 elif num <= 66 : 
    return ("⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜ 66%")
 elif num <= 67 : 
    return ("⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜  67%")
 elif num <= 68 : 
    return ("⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜  68%")
 elif num <= 69 : 
    return ("⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜  69%")
 elif num <= 70 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜ 70%")
 elif num <= 71 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜ 71%")
 elif num <= 72 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜ 72%")
 elif num <= 73 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜ 73%")
 elif num <= 74 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜ 74%")
 elif num <= 75 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜ 75%")
 elif num <= 76 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜ 76%")
 elif num <= 77 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜ 77%")
 elif num <= 78 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜ 79%")
 elif num <= 80 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜  80%")
 elif num <= 81: 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜  81%")
 elif num <= 82 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜  82%")
 elif num <= 83 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜  83%")
 elif num <= 84 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜  84%")
 elif num <= 85 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜  85%") 
 elif num <= 86 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜  86%")
 elif num <= 87 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜  87%")
 elif num <= 88 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜  88%")
 elif num <= 89 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜  89%")
 elif num <= 90 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜ 90%")
 elif num <= 91 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜ 92%")
 elif num <= 93 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜ 93%")
 elif num <= 94 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜ 94%")
 elif num <= 95 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜ 95%")
 elif num <= 96 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜ 96%")
 elif num <= 97 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜ 97%")
 elif num <= 98 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜ 98%")
 elif num <= 99 : 
    return ("⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜ 99%")
 elif num <= 100 : 
    return (" ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛ 100%")
 else:
    return ("⣿⣿⣿⣿⣿ broke my counter! just kidding. I will now recalibrate to the next ATH 1,000,000") 

def bottom():
   return '\n\n $'+ str(bit_current)+'        '+ 'eth/btc: '+ str(price_data())
                                                                     
    
def stat ():
   return checkpercent() + bitcoinData() + bottom()

#login to the bot via Tweepy
auth = tweepy.OAuthHandler("ohhDfWrezyQXuEwslgw7Jhr9H", "q3Z0LzTprwPbwAntUmd6pS7150Eb8MFrEqPpuaTgiGx7aAiarQ")
auth.set_access_token("1126776989266792448-zcHyNmqUzHDt4VhAbpd87ZlnTd35qN", "7nd1ngRXZRhHdecCxZwT8yI3ZU0c8GuTcpn7bXrCFfagi")


start_time = datetime.datetime.now()
interval = start_time + datetime.timedelta(minutes=30)

# dynamically create the interval times
tweet_times = [start_time.minute, interval.minute]

while True:
    current_time = datetime.datetime.now()
    if current_time.minute in tweet_times:
        # your function that tweets
        api = tweepy.API(auth)
        api.update_status (stat())
        # sleep to avoid running the function again in the next loop
        time.sleep(120)
