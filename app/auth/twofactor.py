from random import randint


class Otp:

    otp = randint(1111, 9999)

    @classmethod
    def generate_otp(cls):
        return cls.otp

    @classmethod
    def verify_otp(cls, user_otp: int):
        if cls.otp == user_otp:
            return True
        else:
            return False
