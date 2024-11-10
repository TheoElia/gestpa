from django.conf import settings
import requests
from datetime import datetime


def send_sms(to_number, body):
    account_sid = settings.WIREPICK_ACCOUNT_SID
    account_password = settings.WIREPICK_ACCOUNT_PASSWORD
    from_sid = settings.WIREPICK_ACCOUNT_SID

    data = {
        'client': account_sid,
        'password': account_password,
        'from': from_sid,
        'phone': to_number,
        'text': body,
    }

    result = requests.get(settings.WIREPICK_ENDPOINT, params=data)
    print(f'sent sms {to_number} : {body}  \n\n\n {result.content}')
    return result


def send_sms_transaction_status(user, phone_number, status):
    message_body = "Hi, your transaction status is " + status
    send_sms(phone_number, message_body)


def send_sms_verification_code(user, phone_number, code):
    message_body = f"From GEA ONLINE: \n" \
                   f"One-Time Code: {code}. Code expires in 10 minutes.\n" \
                   f"Reminder: DO NOT SHARE THIS CODE. We will NEVER " \
                   "call you or text you for it."
    send_sms(phone_number, message_body)


def send_sms_cashpayment_token(user, phone_number, code):
    message_body = f"From GEA ONLINE: \n" \
                   f"CASH PAYMENT TOKEN: {code}. Present this code at your selected bac office.\n" \
                   f"Reminder: DO NOT SHARE THIS CODE. We will NEVER " \
                   "call you or text you for it."
    send_sms(phone_number, message_body)


def send_sms_cashpayment_receipt(receipt, phone_number):
    message_body = f"From GEA ONLINE: \n" \
                   f"CASH PAYMENT RECEIPT: You have successfully made a cash payment amount of GHC{receipt.amount}.\nYour receipt number is {receipt.receipt_no}.\nPlease keep this safe for future reference\n"
    send_sms(phone_number, message_body)


def send_sms_secret_code(user, phone_number, code):
    code_to_send =  f'GEA-{code}-{user.month_joined}{user.year_joined}'
    message_body = f"From GEA ONLINE:\n" \
                   f"SECRET LOGIN PIN:\n{code_to_send}\nUse this code for logins\n" \
                   f"Reminder: DO NOT SHARE THIS CODE. We will NEVER " \
                   "call you or text you for it."
    send_sms(phone_number, message_body)


def send_sms_transaction_successful_to_client(phone_number, client_name):
    message_body = f"From GEA ONLINE: \n" \
                   f"Dear {client_name}, We have successfully received your payment. Thank you."
    send_sms(phone_number, message_body)


def send_sms_transaction_failed_to_client(phone_number, client_name):
    message_body = f"From GEA ONLINE: \n" \
                   f"Dear {client_name}, Your payment failed. Please retry the payment. Thank you."
    send_sms(phone_number, message_body)
