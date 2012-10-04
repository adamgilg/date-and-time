#responds to SMS message with sunset or sunrise times for San Francisco.
#user can choose sunset or sunrise by texting a message including the word 'sunset' or 'sunrise in the body.
from flask import Flask, request, redirect
import twilio.twiml
import requests
from bs4 import BeautifulSoup

#pulls in data from website - here set to San Francisco
def handle_response(response_hook):
	#uses requests and Beautiful Soup to bring in text in HTML	
	a = requests.get('http://www.timeanddate.com/worldclock/astronomy.html?n=224')
	soup = BeautifulSoup(a.text)
	result = ""
	#determines which specific lines from HTML to use and how many to display	
	for row in soup('table', {'class' : 'spad'})[0].tbody('tr')[0:3]:
  		tds = row('td')
 		#creates final layout of SMS message
		result += tds[0].string + ' ' + response_hook(tds) + "\n"
	return result

#next two functions point to specific sunset/sunrise data in HTML from website
def sunset(tds):
	return tds[2].string 

def sunrise(tds):
	return tds[1].string 

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])

#determines whether to respond to incoming SMS with sunrise or sunset times
def sms_response():
	resp = twilio.twiml.Response()
	#responds if sunset or sunrise appear anywhere in the message, in upper or lower case
	#defaults to sunset if both are included
	if 'sunset' in request.form['Body'].lower():
		resp.sms(handle_response(sunset))
	elif 'sunrise' in request.form['Body'].lower():
		resp.sms(handle_response(sunrise))
	#instructs user in case neither word is received	
	else:
		resp.sms('Text \'sunrise\' or \'sunset\' for San Francisco sunrise/sunset times')
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)


