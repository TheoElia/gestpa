class SMSTemplate:
    def __init__(self):
        pass

    def welcome(self,otp):
        message = f"""Welcome to Pharst Care, this is your one time password(OTP): {otp}, use it to verify your phone number."""
        return message


    def forgotten_password(self,token):
        message = f"""Please use this link to reset your password https://www.pharst.care/accounts/reset-password/{token}"""
        return message


    def consultation_doctor_initial_message(self,contact,order_id):
        message = f"A client logged a complaint, contact {contact}, link https://www.pharst.care/health/doctor-consultation-room/{order_id}/"
        return message


    def consultation_client_initial_message(self,order_id):
        message = f"""Hello, we have received your complaint and a doctor will be in touch soon. Access your consultation room directly in the Pharst Care app (swipe left on the home screen) or visit https://pharst.pywe.org/health/client-consultation-room/{order_id}/"""
        return message