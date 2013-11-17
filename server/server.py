from flask import Flask, request, redirect
#import twilio.twiml
#from twilio.rest import TwilioRestClient
import sendgrid

app = Flask(__name__)
DOMAIN_NAME = "ess@nator.com"

@app.route("/", methods=['GET', 'POST'])
def index():
	return "Hello world!"


@app.rout("/essanator", methods=['GET', 'POST'])

def send_email(address, name, subject, message):
    s = sendgrid.Sendgrid("Mister_Abc", "xXxXxXxXxXx", secure=True)
    # TODO !!! GET RID OF MY PASSWORD BEFORE MAKING PUBLIC !!! TODO #
    email = sendgrid.Message(DOMAIN_NAME, subject, message, "")
    email.add_to(address, name)
    print("Sending message to %s; %s"%name, address)
    print("Subject: %s", subject)
    print(message)

    s.web.send(email)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4414, debug=True)
