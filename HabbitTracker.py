import requests, json, time, re, datetime, smtplib, ssl

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
	
#set start date of habits
start_date = datetime.datetime(2021, 1, 31)

now_date = datetime.datetime.now()

#Subtract the current date from the start date
days_elapsed = str(now_date - start_date).split(",")[0]

#email a text to myself at 5 pm every day notifying me of what day I'm on and give me a message to keep going
port = 465 # For SSL
password = "Password" #Change this at runtime

sender_email = "curtspython@gmail.com"
receiver_email = "PhoneNumber@txt.att.net"

message = """\
Subject: Daily Habit Tracker

Congratulations Curtis, you've made it another day working on:
1. Python Coding
2. Exercising
3. Cooking


Continue your work; you're doing well!

Your current counter is {}
""".format(days_elapsed)

#create secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("curtspython@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)
