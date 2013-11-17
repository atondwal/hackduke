from flask import Flask, request, redirect,url_for
import twilio.twiml as twiml
from twilio.rest import TwilioRestClient
import sendgrid
import drunkuncle
import goog
import re, uuid, os, sys, subprocess

app = Flask(__name__,static_folder='static', static_url_path='/static')
DOMAIN_NAME = "twist@twist.bymail.in"

@app.route("/", methods=['GET', 'POST'])
def index():
    page = '''
           <html>
           <body>
           <h1> I'm not drunk, I'm just....shut up. </h1>
            <form action="/twist" method="POST">
                <input type="hidden" name="from" value="Website"/>
                <input type="text" name="text" value="Well, what do you think?"/>
                <input type="submit" value="Say that one more time, I dare you!"/>
            </form>
            </body>
            </html>
    '''
    return page

s = sendgrid.Sendgrid('username', 'password', secure=True)
pat = re.compile("(.*)<(.*)>$")

@app.route("/twist", methods=['GET', 'POST'])
def twist():
    match = pat.match(request.form['from'])
    if match is not None:
        name = match.group(1)
        from_email = match.group(2)
    else:
        name="Website"
        from_email="Website"
    #['from', 'attachments', 'headers', 'text', 'envelope', 'to', 'html', 'sender_ip', 'subject', 'dkim', 'SPF', 'charsets']
    body = "".join(request.form['text'])
    print("Email has body: %s" % body)
    (mp3file, body) = parse(body)
    insult=subprocess.check_output('./insult.sh')
    #text2mp3(mp3file,insult)
    #text2mp3(uuid.uuid1().hex + ".mp3", insult)
    print("We return: %s"%body)
    if from_email != "Website":
        send_email(from_email, name, "From HackDuke with love...", body, mp3file)
        return ""
    else:
        page = '''
           <html>
           <body>
           <h1> ''' + insult+ '''</h1>
           '''  +body+'''
            <form action="/twist" method="POST">
                <input type="hidden" name="from" value="Website"></input>
                <input type="text" name="text" value="Well, what do you think?"/>
                <input type="submit" value="Say that one more time, I dare you!"/>
            </form>
            </body>
            </html>     
            '''
        return page


def send_email(address, name, subject, message, attachment = None):
    s = sendgrid.Sendgrid("Mister_Abc", "xXxXxXxXxXx", secure=True)
    # TODO !!! GET RID OF MY PASSWORD BEFORE MAKING PUBLIC !!! TODO #
    email = sendgrid.Message(DOMAIN_NAME, subject, message, message)
    email.add_to(address, name)
    print("Sending message to %s; %s"%(name, address))
    print("Subject: %s"%subject)
    print(message)
    if attachment and os.path.isfile(attachment):
        email.add_attachment(os.path.basename(attachment), attachment)
        print("Attaching %s..."%os.path.abspath(attachment))

    s.web.send(email)
    print("Deleting %s..."%os.path.abspath(attachment))
    if os.path.isfile(attachment):
        os.remove(attachment)

    
account_sid = "xXxXxXxXxXx" # TODO: read from file
auth_token = "xXxXxXxXxXx" # TODO: read key from file
client = TwilioRestClient(account_sid, auth_token)


@app.route("/twilio", methods=['GET', 'POST'])
def twilio():
    resp = twiml.Response()
    messages = client.messages.list()
    message = messages[0]
    (mp3file, rspv) = parse(message.body)
    if os.path.isfile(mp3file):
        os.remove(mp3file)
    print(rspv)
    resp.message(rspv)
    return str(resp)


app.config['parser'] = drunkuncle.DrunkUncle()

def parse(text):
    text=''.join(text)
    text = goog.relevant_passage(text, app.config['parser'])
    filename = "" #text2mp3(uuid.uuid1().hex + ".mp3", text)
    return (filename, text)

def text2mp3(filename, text):
    text=''.join(text)
    pipe = subprocess.Popen(['./text2mp3.zsh',"static/"+filename],stdin=subprocess.PIPE)
    print("Turning text to mp3:\n%s"%text)
    #pipe.communicate(text)
    return filename

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4414, debug=True)
