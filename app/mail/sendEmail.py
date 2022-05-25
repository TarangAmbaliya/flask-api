from app.mail import mail
from flask_mail import Message
from flask import render_template


class Email:
    def __init__(self,
                 sender='testapp@flask.com',
                 subject='This is a test mail',
                 recipients='tarangambaliya@gmail.com'):

        self.sender = sender
        self.subject = subject
        self.receipients = recipients

    def send_welcome_email(self):
        msg = Message(sender=self.sender, subject=self.subject, recipients=self.receipients)
        msg.html = render_template('welcome.html')
        mail.send(msg)
