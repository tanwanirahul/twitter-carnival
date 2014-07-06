'''
Created on 05-Jul-2014

@author: Rahul

@summary: Contains the notification service if the configured number
          of photos has been accumulated.
'''
import smtplib
from email.mime.text import MIMEText


class EmailNotification(object):

    '''
        Encapsulates the Email Notification tasks.
    '''

    def __init__(self, host, port, sender_email, sender_password):
        '''
            Configure our SMTP client.
        '''
        self.sender_email = sender_email
        self.password = sender_password
        host = host
        port = port
        self.smtp_obj = smtplib.SMTP(host, port)
        self.smtp_obj.ehlo()
        self.smtp_obj.starttls()
        self.smtp_obj.ehlo()
        self.smtp_obj.login(self.sender_email, self.password)

    def send(self, subject, message, from_name, from_email, to, bcc,
             **options):
        '''
            Sends email notification based on the provided email configuration.
        '''
        recievers = [to] + [bcc]
        msg = self.prepare_message(from_name, from_email, to, bcc,
                                   subject, message, **options)
        if msg is None:
            return
        self.smtp_obj.sendmail(self.sender_email, recievers, msg)

    def prepare_message(self, sender_name, sender, to, bcc, subject,
                        message, **temp_options):
        '''
             Prepares and returns the message that needs to be sent.
        '''
        if to is None and bcc is None:
            return
        message = message.format(**temp_options)
        subject = subject.format(**temp_options)

        msg = MIMEText(message)
        msg["subject"] = subject
        msg["from"] = "{0} <{1}>".format(sender_name, sender)
        msg["to"] = "<{0}>".format(to)
        msg["bcc"] = "<{0}>".format(bcc)

        return msg.as_string()
