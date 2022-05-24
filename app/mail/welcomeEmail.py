from app.mail import mail
from flask_mail import Message
from flask import render_template


class Email:
    def __init__(self, subject, template):
        self.subject = subject
        self.template = template

    @staticmethod
    def send_email():
        msg = Message()
        msg.html = render_template('welcome.html')
        mail.send(msg)
