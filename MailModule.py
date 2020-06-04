import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    
    How are you? I hope you had been an amazing week and the weekend is even better:)
    
    According to my scripts, in order of certainty on my script, here are the predictions for what stock will grow in the next 3 weeks:
    The biggest chances to succeed: {} 
    The second priority would be: {}
    And the ones predicted by our weakest script are: {}
    Hope you make money out of these script predictions.
        
    Best regards,
    Simion
    
    -----------------------------------------------------------------------------------------------------------------------------------------------
    According to backtest on the weakest script we still have a 70% chance of growth over the next 3 weeks. The other two are better 
    
    *if in some category there are no stocks written it means the script doesn't consider any stock to be good enough
    **Disclaimer: I have no education in finance and you should do your investing and trading based on your own due dilligence and research. 
    All this recommendation should be taken with a grain a salt and a critical mind. I will invest in some of the positions mentioned above.
    """.format(name, both, category, priceprediction)

    print(body)
    return body


def send_mail(both, category, pricepredict):
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

        # send the message via the server set up earlier.
        mail.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    mail.quit()

