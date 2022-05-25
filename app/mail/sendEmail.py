from app.mail import mail
from flask_mail import Message
from flask import render_template


class Email:
    def __init__(self,
                 name: str = 'User',
                 sender: str = 'testapp@flask.com',
                 subject: str = 'This is a test mail',
                 recipients: str | list = 'tarangambaliya@gmail.com',
                 template: str = 'welcome.html',
                 otp: int = ''):

        self.name = name
        self.sender = sender
        self.subject = subject
        self.receipients = recipients
        self.template = template
        self.otp = otp

    def send_email(self):
        msg = Message(sender=self.sender, subject=self.subject, recipients=self.receipients)
        msg.html = render_template(self.template, name=self.name, otp=self.otp)
        mail.send(msg)
