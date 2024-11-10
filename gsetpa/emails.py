from django.conf import settings
from django.core.mail import EmailMessage


def send_email(email, template_id, data):
    mail = EmailMessage(from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
    mail.content_subtype = 'html'
    mail.template_id = template_id
    mail.dynamic_template_data = data
    # print(email, data)
    mail.send(fail_silently=True)


def send_bulk_email(emails, template_id, data):
    mail = EmailMessage(from_email=settings.DEFAULT_FROM_EMAIL, to=emails)
    mail.content_subtype = 'html'
    mail.template_id = template_id
    mail.dynamic_template_data = data
    # print(email, data)
    mail.send(fail_silently=True)


def send_verification_code_email(user, email, code):
    template_id = settings.VERIFICATION_CODE_EMAIL_ID
    params = {"first_name": user.first_name if user else '', "code": code, "url": settings.ADMIN_LINK}
    return send_email(email, template_id, params)


def send_verification_link_email(user, email, link):
    template_id = settings.VERIFICATION_LINK_EMAIL_ID
    params = {"first_name": user.first_name if user else '', "link": link}
    return send_email(email, template_id, params)


def send_set_new_account_email_link_email(user, email, link):
    template_id = settings.SET_NEW_ACCOUNT_EMAIL_LINK_EMAIL_ID
    params = {"first_name": user.first_name if user else '', "link": link}
    return send_email(email, template_id, params)


def send_welcome_email(user):
    template_id = settings.WELCOME_EMAIL_ID
    params = {"first_name": user.first_name}
    return send_email(user.temp_email, template_id, params)


def send_transaction_status_email(user, transaction):
    template_id = settings.TRANSACTION_STATUS_EMAIL_ID
    params = {"first_name": user.first_name,
              "recipient_first_name": transaction.recipient.first_name,
              "recipient_account": transaction.recipient_account.account_type,
              "transaction_status": transaction.status}
    return send_email(user.email, template_id, params)


def send_password_reset_email(user, email, code):
    template_id = settings.PASSWORD_RESET_EMAIL_ID
    params = {"first_name": user.first_name, "code": code}
    return send_email(email, template_id, params)

def send_locked_account_password_reset_email(user, email, code):
    template_id = settings.ACCOUNT_LOCKED_ALERT_EMAIL_ID
    params = {"first_name": user.first_name, "code": code,"url":f"{settings.ADMIN_LINK}reset-password"}
    return send_email(email, template_id, params)


def send_membership_approved_status_email(member):
    template_id = settings.APPROVAL_ACCEPTED_ALERT_EMAIL_ID
    params = {"first_name": member.first_name, "link": settings.WEB_LINK}
    return send_email(member.email, template_id, params)


def send_membership_rejected_status_email(member):
    template_id = settings.APPROVAL_DECLINED_ALERT_EMAIL_ID
    params = {"first_name": member.first_name, "link": settings.WEB_LINK}
    return send_email(member.email, template_id, params)


def send_regional_approval_email(user,members):
    template_id = settings.REGIONAL_APPROVAL_EMAIL_ID
    params = {"phone_number":f"{user.phone_number}","dashboard_url":settings.ADMIN_LINK}
    return send_bulk_email([member.email for member in members], template_id, params)


def send_head_office_approval_email(user,members):
    template_id = settings.REGIONAL_APPROVAL_EMAIL_ID
    params = {"phone_number":f"{user.phone_number}","dashboard_url":settings.ADMIN_LINK}
    return send_bulk_email([member.email for member in members], template_id, params)