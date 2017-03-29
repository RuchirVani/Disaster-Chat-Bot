from flask import Flask, request, redirect,session
import twilio.twiml
import boto3
import random,string
from twilio.rest import TwilioRestClient
import csv



callers = {
    "+18572141901": "Admin",
    "+18573897908":"Admin2",
    "+17329796830":"Admin3",
    "+15617620868":"Admin4",
    "+13128003133":"Admin5",
}
#SECRET_KEY = 'a secret key'

#counter=0

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    counter = session.get('counter', 0)
    from_number = request.values.get('From', None)
    counter += 1
    session['counter'] = counter
    session['from']=from_number
    resp = twilio.twiml.Response()
    if from_number in callers:

    	print('Response : '+request.values.get('Body', None))
    	print('Counter : '+ str(counter))

        if request.values.get('Body', None)=='Y' and counter==1:
        	resp.message("Ok, We will require an additional 3 doctors ad 3 nurses. Should I start Sending invites based on priority?(Y/N)")
        	return str(resp)
        elif request.values.get('Body', None)=='Y' and counter==2:
        	resp.message("Thanks!! I am sending emails to staff")
        	listOfStaff=sendToStaff()
        	account_sid = "AC81c407d9152bfe89bb5a914ab58a9b65" # Your Account SID from www.twilio.com/console
        	auth_token  = "71f6eab1e135bf8dcb3ade88821077da"  # Your Auth Token from www.twilio.com/console
        	client = TwilioRestClient(account_sid, auth_token,base="https://api.twilio.com:8443")
        	counter_to_send=0
        	for to_number in listOfStaff:
				if counter_to_send<5:
					client = TwilioRestClient(account_sid, auth_token,base="https://api.twilio.com:8443")
					message = client.messages.create(body='''Huricane Katrina is approching and we need to increase staff at MGH. Can you accept a shift at 8.00 AM on 3/30/2017?''',to="+1"+str(to_number),from_="+14843194502")
					counter_to_send=counter_to_send+1
        	return str(resp)
        elif request.values.get('Body', None)=='Yes':
        	resp.message("Great, See you tomorrow.")
        	return str(resp)
        elif request.values.get('Body', None)=='No' and (counter==2 or counter==1):
        	resp.message("Ok, No problem!! Can you do a shift tomorrow at 4.00 AM?")
        	return str(resp)
        elif request.values.get('Body', None)=='No' and counter>4:
        	resp.message("Ok, No problem!!")
        	return str(resp)
        else :
        	resp.message("Sorry, I didnt get that!! Can you please say Yes or No?")
        	return str(resp)

    return str(resp.message("Sorry, I didnt get that!! Can you please say Yes or No?"))


def sendToStaff():
	#TODO:Send an msgs to Staff

	# read from database to find the best contact
	listOfStaff=[]
	rownum = 0	
	with open('Disaster_Bot2.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)

		for row in reader:
			if rownum ==0:
				print('header')
			else:
				listOfStaff.append(row[2])
			rownum=rownum+1

	return listOfStaff
	# creatlist based on score
	'''score=10.0
	for person in listOfStaff:
		if(score>person[12]):
			score=person[12]
'''

	#print(message.sid)
	#session.clear()

if __name__ == "__main__":
	app.secret_key = ''.join(random.choice(string.lowercase) for i in range(10))
	app.run(debug=True)
	session.clear()