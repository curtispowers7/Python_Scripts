#Sends a text notification through gmail when it is a full moon


import pandas as pd
import datetime
import smtplib
import ssl

attrs = {
    "class":"tb-sm zebra fw tb-hover"
}
year = str(datetime.datetime.today().year)
url = "https://www.timeanddate.com/moon/phases/usa/monterey?year=" + year

table_moon = pd.read_html(url, attrs = attrs)

tb = table_moon[0]

strDates = list(tb[tb["Full Moon"].str.match('[A-Z][a-z]{2} [0-9]{1,2}') == True]['Full Moon'])

dates = []
for p in strDates:
    dates.append(datetime.datetime.strptime(p + " " + year, "%b %d %Y").date())


for date in dates:
    if date == datetime.datetime.today().date():
        port = 465 # For SSL
        password = "Password" #Replace this at runtime

        sender_email = "curtspython@gmail.com"
        receiver_email = "PhoneNumber@txt.att.net"

        message = """\
        Subject: Full Moon Drink!

        Hey Curtis, 
        Tonight is a full moon, go ahead and enjoy yourself a couple drinks or four!
        """

        #create secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("curtspython@gmail.com", password)
            server.sendmail(sender_email, receiver_email, message)
