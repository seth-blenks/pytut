
import random
from flask import Flask, request
from pymessenger.bot import Bot
import json

app = Flask(__name__)

ACCESS_TOKEN = 'EAAGdKbZB2WMUBANIXXq6zqGTTD0fYoZCNGogb7fiwxNOd1nJIEjRwxjQLelnGwOvsUda3CThYfRGZANr8wD8cUfxo0rUHBkZCCUrZBLOGVWXckQyJn4ZB0WIyzvxorZCGAm4Ui0Rkofs887lQtKtraAc9aIIZAa8uyaNHhCIYJcwOQZDZD'
VERIFY_TOKEN = 'TESTSECRETTOKEN'
bot = Bot(ACCESS_TOKEN)

#FACEBOOK_APP_ID=454277612329157
#PAGE_ACCESS_TOKEN=EAAGdKbZB2WMUBAC4zKUOHZAjhh158hrYOLEbKzYSmZARThipHhxZCLgHfmtHXAjVoZCp9GLCEEP07TO2wlwnjRZA6M9rgMb8FLeKInPDxJ85Xzu3MiSOYSd3eIZAsZCcf9QhGSO1PZCUS3kkZCcuAYalL9PqDtm1Ox49i1oxaeXo8ZBoAZDZD
#PAGE_ID=109122367456761

@app.route('/',methods=['GET','POST'])
def receive_message():
    if request.method == 'GET':
        # Before allowing people to message your bot, Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook. 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message # back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        with open('data.txt','w') as wfile:
        	wfile.write(json.dumps(output))
        for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

if __name__ == '__main__':
	app.run()