from flask import Flask, request, redirect
import twilio.twiml as twiml
from twilio.rest import TwilioRestClient
import sendgrid
import re, uuid

app = Flask(__name__)
DOMAIN_NAME = "twist@twist.bymail.in"

@app.route("/", methods=['GET', 'POST'])
def index():
	return "Hello world!"


s = sendgrid.Sendgrid('username', 'password', secure=True)
pat = re.compile("(.*)<(.*)>$")

@app.route("/twist", methods=['GET', 'POST'])
def twist():
    match = pat.match(request.form['from'])
    name = match.group(1)
    from_email = match.group(2)
    #['from', 'attachments', 'headers', 'text', 'envelope', 'to', 'html', 'sender_ip', 'subject', 'dkim', 'SPF', 'charsets']
    body = request.form['text']
    parse(body)
    send_email(from_email, name, "From HackDuke with love...", body)
    return ""


account_sid = "xXxXxXxXxXx" # TODO: read from file
auth_token = "xXxXxXxXxXx" # TODO: read key from file
client = TwilioRestClient(account_sid, auth_token)


@app.route("/twilio", methods=['GET', 'POST'])
def twilio():
    resp = twiml.Response()
    messages = client.messages.list()
    message = messages[0]
    rspv = parse(message.body)
    print(rspv)
    resp.message(rspv)
    return str(resp)


def send_email(address, name, subject, message):
    s = sendgrid.Sendgrid("Mister_Abc", "xXxXxXxXxXx", secure=True)
    # TODO !!! GET RID OF MY PASSWORD BEFORE MAKING PUBLIC !!! TODO #
    email = sendgrid.Message(DOMAIN_NAME, subject, message, message)
    email.add_to(address, name)
    print("Sending message to %s; %s"%name, address)
    print("Subject: %s", subject)
    print(message)

    s.web.send(email)


def parse(text):
    return text # TODO you know, parse the text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4414, debug=True)
