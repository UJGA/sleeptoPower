import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
import json
import smtplib

CLIENT_ID = '22C7HQ'
CLIENT_SECRET = '0fccacdc442bfad5d81edf326fb96bcf'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y%m%d"))

fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=yesterday2, detail_level='1sec')

steps = auth2_client.activities(date=None, user_id=None, data=None,)

stepJson = json.dumps(steps)

loadJson = json.loads(stepJson)

activities = loadJson['activities']

for thing in activities:
    stepString = thing['steps']
    stepInt = int(stepString)

print(stepInt)

goal = 1000

if stepInt > goal:

    gmail_user = 'blakeriding@gmail.com'
    gmail_password = 'eowinkdtijkkagfi'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    except:
        print('Something went wrong...')

    sent_from = 'blakeriding@gmail.com'
    to = ['blake.riding498@gmail.com']
    subject = 'Step Count Hit'
    body = 'You hit your step goal!'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)


    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')