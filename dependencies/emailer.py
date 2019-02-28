# -*- coding: utf-8 -*-
import os
import sys
import time
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


__DIR__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, __DIR__ + "/../")

import logger



class Emailer:

    def __init__(self):
        pass
    
    
    #
    # Def send email
    #
    def send(self, username, password, subject, to, text):
        try:
            msg = MIMEMultipart()

            msg['From'] = username
            msg['To'] = to
            msg['Subject'] = subject

            msg.attach(MIMEText(text, 'html'))

            mail_server = smtplib.SMTP('smtp.gmail.com', 587)
            mail_server.ehlo()
            mail_server.starttls()
            mail_server.ehlo()
            mail_server.login(username, password)
            mail_server.sendmail(username, to, msg.as_string())
            mail_server.close()

            return True
        except:
            logger.dump("send_email(%s, %s): %s" %(to, subject, str(sys.exc_info())), 'critical')
        

        return False 
    



if __name__ == "__main__":
    e = Emailer()
    e.send('', '', 'ASD Test', 'dpanic@gmail.com', 'this is a test')
