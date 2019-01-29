# mopac-price.py
#!/usr/bin/python

#
# 
# You could use this script to map the real time travel times of the past day (cron job, every minute)
# To plot grpahs you could use: http://plot.ly
#
#
import time
import simplejson
import urllib
import json
from datetime import datetime
from blink1.blink1 import Blink1
import requests

b1 = Blink1()
try:
	while True:
		date = datetime.now()
		date1 = date.strftime("%m/%d/%Y %H:%M")

# Create the POST request
		data = {'starttime' : date1}
		requests.packages.urllib3.disable_warnings()

		headers = {
   		'$Host': 'mopac-fare.mroms.us',
    		'$User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    		'$Accept': 'application/json, text/javascript, */*; q=0.01',
    		'$Accept-Language': 'en-US,en;q=0.5',
    		'$Accept-Encoding': 'gzip, deflate',
    		'$Referer': 'https://www.mobilityauthority.com/pay-your-toll/current-mopac-rates',
    		'$Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    		'$Origin': 'https://www.mobilityauthority.com',
    		'$Connection': 'close',
		}

		response = requests.post('https://mopac-fare.mroms.us/HistoricalFare/ViewHistoricalFare', headers=headers, data=data, verify=False)

		price = response.text
		price2 = json.loads(price)
		print (date1)
		finalprice = (price2[1]['tripRate'])
		print (finalprice)

# Append results to the file
		target = open("Results.csv", 'a')
		target.write(datetime.now().strftime('%m-%d-%Y %H:%M') + ";$"+ str(finalprice) + "\n")
		target.close()

# Make it Flash Color
		if finalprice <= 1.00:
			b1.fade_to_rgb( 100, 0,255,0 )
			time.sleep(30)
		elif finalprice >= 1.00 and finalprice <= 4.00:
			b1.fade_to_rgb( 100, 255,255,0 )
			time.sleep(30)
		elif finalprice >= 4.01:
			b1.fade_to_rgb( 100, 255,0,0 )
			time.sleep(30)
except:
	b1.fade_to_rgb( 100, 0,0,0 )
	print ("Error!")
