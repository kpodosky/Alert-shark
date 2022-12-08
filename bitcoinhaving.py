# -*- coding: utf-8 -*-
import requests
import time
import tweepy
import datetime
from datetime import timedelta
from datetime import datetime

tuple1 = ("░")
tuple2 = ("█")
tuple3 = ("▒")
    
def halving():
    
 
 futuredate = datetime.strptime('May 14 2020  04:49:56', '%b %d %Y %H:%M:%S')

 nowdate = datetime.now()
 count = int((futuredate-nowdate).total_seconds())

 if nowdate <= futuredate :
  futuredate =  datetime.strptime('May 24 2028  04:49:56', '%b %d %Y %H:%M:%S')
   
 days = count//86400
 hours = (count-days*86400)//3600
 minutes = (count-days*86400-hours*3600)//60
 seconds = count-days*86400-hours*3600-minutes*60
 day = days
 def timing():
    return("{} 𝚍𝚊𝚢𝚜 {} 𝚑𝚛𝚜 {} 𝚖𝚒𝚗𝚜 (to #btc halving)".format(days, hours, minutes, seconds))
 
 def chart():
   if day <= 0:
    return (tuple1*20 +' 0%' )
   elif day <= 70:
    return (tuple1*19 + tuple2*1 +' 5%')
   elif day <= 141:
    return (tuple1*18 + tuple2*2+' 10%')
   elif day <= 211:
    return (tuple1*17 + tuple2*3+' 15%')
   elif day <= 281:
    return (tuple1*16 + tuple2*4+' 20%')
   elif day <= 351:
    return (tuple1*15 + tuple2*5+' 25%')
   elif day <= 422:
    return (tuple1*14 + tuple2*6+' 30%')
   elif day <= 492:
    return (tuple1*13 + tuple2*7+' 35%')
   elif day <= 562:
    return (tuple1*12 + tuple2*8+' 40%')
   elif day <= 632:
    return (tuple1*11 + tuple2*9+' 45%')
   elif day <= 703:
    return (tuple1*10 + tuple2*10+' 50%')
   elif day <= 773:
    return (tuple1*9 + tuple2*11+' 55%')
   elif day <= 843:
    return (tuple1*8 + tuple2*12+' 60%')
   elif day <= 913:
    return (tuple1*7 + tuple2*13+' 65%')
   elif day <= 984:
    return (tuple1*6 + tuple2*14+' 70%')
   elif day <= 1054:
    return (tuple1*5 + tuple2*15+' 75%')
   elif day <= 1124:
    return (tuple1*4 + tuple2*16+' 80%')
   elif day <= 1195:
    return (tuple1*3 + tuple2*17+' 85%')
   elif day <= 1265:
    return (tuple1*2  + tuple2*18+' 90%')
   elif day <= 1335:
    return (tuple1  + tuple2*19+' 95%')
   elif day < 1405 :
    return (tuple2* 20 +' 100%')
 
 return str(chart() +'\n\n'+ timing())

#login to the bot via Tweepy
auth = tweepy.OAuthHandler("ohhDfWrezyQXuEwslgw7Jhr9H", "q3Z0LzTprwPbwAntUmd6pS7150Eb8MFrEqPpuaTgiGx7aAiarQ")
auth.set_access_token("1126776989266792448-zcHyNmqUzHDt4VhAbpd87ZlnTd35qN", "7nd1ngRXZRhHdecCxZwT8yI3ZU0c8GuTcpn7bXrCFfagi")


start_time = datetime.now()
interval = start_time + timedelta (days=2)

# dynamically create the interval times
tweet_times = [start_time.minute, interval.minute]

while True:
    current_time = datetime.now()
    if current_time.minute in tweet_times:
        # your function that tweets
        api = tweepy.API(auth)
        api.update_status (halving())
        # sleep to avoid running the function again in the next loop
        time.sleep(120)
        
print (halving()) 