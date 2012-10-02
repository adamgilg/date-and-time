from flask import Flask, request, redirect
import twilio.twiml
import requests
from bs4 import BeautifulSoup

def handle_response(response_hook):
	a = requests.get('http://www.timeanddate.com/worldclock/astronomy.html?n=224')
	soup = BeautifulSoup(a.text)
	result = ""
	for row in soup('table', {'class' : 'spad'})[0].tbody('tr')[0:3]:
  		tds = row('td')
 		result += tds[0].string + ' ' + response_hook(tds) + "\n"
	return result

def sunset(tds):
	return tds[2].string 

def sunrise(tds):
	return tds[1].string 

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond to incoming calls with a simple text message."""
	resp = twilio.twiml.Response()
	if 'sunset' in request.form['Body'].lower():
		resp.sms(handle_response(sunset))
	elif 'sunrise' in request.form['Body'].lower():
		resp.sms(handle_response(sunrise))
	else:
		resp.sms('Text \'sunrise\' or \'sunset\' for San Francisco sunrise/sunset times')
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)


