from random import randint


class Otp:

    def __init__(self):
        self.otp = randint(1111, 9999)
        self.email = ''

    def generate_otp(self, email):
        self.email = email
        return self.otp

    def verify_otp(self, otp, email):
        if email == self.email:
            if int(otp) == self.otp:
                return True
            else:
                return False
