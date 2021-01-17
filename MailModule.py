import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import ReportModule as Rm
import time
from datetime import date

SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SMTP_USERNAME = 'sularea.vasile@yahoo.com'
SMTP_PASSWORD = 'your password here'
EMAIL_FROM = 'sularea.vasile@yahoo.com'


def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def create_mail_body(name, both, category, priceprediction, old_report):
    # Create the plain-text and HTML version of your message
    body = """\
    Hi {},
        
            According to my scripts, in order of certainty on my script, here are the predictions for what stock will grow in the next 3 weeks:
       -Both scripts recommended to succeed- 
    {} 
          -Script no.1 recommended- 
    {}
          -Script no.2 recommended- 
    {}
    Hope you have fun with these script predictions.
    
    Results from 3 weeks ago prediction are:
{}
Best regards,
Simion

*if in some section there are no stocks written (you see this sign [])it means the scripts don't consider any stock to be good enough for that section
**Disclaimer: I have no education in finance and you should do your investing and trading based on your own due dilligence and research.
All this recommendation should be taken with a grain a salt and a critical mind. I will invest in some of the positions mentioned above.
""".format(name, both, category, priceprediction, old_report)

    print(body)
    return body


def send_mail(both, category, pricepredict, file):
    names, emails = get_contacts('mycontacts.txt')  # read contacts
    results = Rm.return_report_from_3_weeks_ago()

    for i in range(10):
        try:
            # set up the SMTP server
            mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            mail.set_debuglevel(True)
            mail.starttls()
            mail.login(SMTP_USERNAME, SMTP_PASSWORD)
            break
        except:
            print("Could not connect")
            time.sleep(30)
            continue
    mails_not_sent = []
    # For each contact, send the email:
    for name, email in zip(names, emails):
        try:
            msg = MIMEMultipart()  # create a message

            # setup the parameters of the message
            msg['From'] = EMAIL_FROM
            msg['To'] = email
            msg['Subject'] = "Predictions of the week " + str(date.today())

            text = create_mail_body(name, both, category, pricepredict, results)

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
            time.sleep(10)
        except:
            mails_not_sent.append(name)
    # Terminate the SMTP session and close the connection
    mail.quit()
    if len(mails_not_sent) > 0:
        with open("log.txt", mode='w+', encoding='utf-8') as file:
            file.write("The following emails have not been sent\n")
            for name in mails_not_sent:
                file.write(name + "\t")
        file.close()
