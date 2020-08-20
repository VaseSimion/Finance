import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SMTP_USERNAME = 'sularea.vasile@yahoo.com'
SMTP_PASSWORD = 'jaxulohkfyajzajp'
EMAIL_FROM = 'sularea.vasile@yahoo.com'


def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def create_mail_body(name, both, category, priceprediction):
    # Create the plain-text and HTML version of your message
    body = """\
    Hi {},
    
	It's been a while since I've put some time into this script. I'm planning to expand the list of stocks and add previous results into these e-mails. It might come next week this update of the next one, bear with me.
	
	According to my scripts, in order of certainty on my script, here are the predictions for what stock will grow in the next 3 weeks:
    The biggest chances to succeed: {} 
    The second priority would be: {}
    And the third priority list is: {}
    Hope you make money out of these script predictions.
    
	As a notification, in this period it seems the market behaves a bit off compared to my model so be cautious.
    
	Best regards,
    Simion
    
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Background:
	I have designed 2 scripts based on machine learning with different approaches. One predicts if the price will rise over 20% or not (in reality is more than that but this is the short version) and the other one tries to predict the exact price increase and from that I pick some based on backtesting.
	If both scripts predict one stock as a winner, this will appear in the "biggest chances to succeed". If only the best script predicts one stock is a winner then it appears in the second priority list. And if only the price prediction script predicts for one stock to grow then it appears in the third priority list.
	According to backtest on the weakest script we still have a 70% chance of growth over the next 3 weeks. The other two are better. 
    The scripts are actually predicting on what is going to happen over the next three weeks. So the strategy is to buy now and hold for 3 weeks. An increase in price of 1.25 in the raport means the script thinks the price will rise with 25%.
	I hope this is clear enough, if not please do not hesitate to contact me at sularea.vasile@gmail.com. The e-mail adress I'm sending the e-mails from will most probabily be seen as spam in the future so I use this yahoo one which is basically used for promotions and spam.
	If you want to see old predictions to check how the script behaved, I have data saved since 23.5.2020. I have more with a variation of this script which are from march but it's not exactly this script so I don't count them as validation.
	
    *if in some category there are no stocks written (you see this sign [])it means the script doesn't consider any stock to be good enough for that category
    **Disclaimer: I have no education in finance and you should do your investing and trading based on your own due dilligence and research.
    ***Penny stocks are more risky then the rest, ignore them if you want to lower your risk 
    All this recommendation should be taken with a grain a salt and a critical mind. I will invest in some of the positions mentioned above.
    """.format(name, both, category, priceprediction)

    print(body)
    return body


def send_mail(both, category, pricepredict, file):
    names, emails = get_contacts('mycontacts.txt')  # read contacts

    # set up the SMTP server
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(True)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message

        # setup the parameters of the message
        msg['From'] = EMAIL_FROM
        msg['To'] = email
        msg['Subject'] = "Predictions of the week"

        text = create_mail_body(name, both, category, pricepredict)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")

        msg.attach(part1)

        # Open report file in binary mode
        with open(file, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file}",
        )

        msg.attach(part)
        # send the message via the server set up earlier.
        mail.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    mail.quit()

