from django.core.mail import send_mail
from django.template.loader import render_to_string
from pathlib import Path

from core.models import EmailTemplate

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class EmailNotification:
    def __init__(self):
        pass

    def email_users_only_emails(self,emails,email_subject,extra_args):
        for email in emails:
            # for test cases email template may not be available
            try:
                welcome_mail = EmailTemplate.objects.get(subject=email_subject)
            except EmailTemplate.DoesNotExist:
                email_html = open(BASE_DIR / "templates/welcome_email.html", "r+")
                email_txt = open(BASE_DIR / "templates/welcome_email.txt", "r+")
                # get current conten in body
                welcome_mail_body = email_html.read()
                welcome_mail_text = email_txt.read()
                email_html.close()
                email_txt.close()
                email_html = open(BASE_DIR / "templates/welcome_email.html", "w+")
                email_txt = open(BASE_DIR / "templates/welcome_email.txt", "w+")
                email_html.write(welcome_mail_body)
                email_txt.write(welcome_mail_text)
                email_html.close()
                email_txt.close()
                msg_plain = render_to_string('welcome_email.txt',extra_args)
                msg_html = render_to_string('welcome_email.html', extra_args)
                subject = "Welcome To Pharstcare"
            else:
                email_html = open(BASE_DIR / "templates/welcome_email.html", "w+")
                email_txt = open(BASE_DIR / "templates/welcome_email.txt", "w+")
                email_html.write(welcome_mail.body)
                email_txt.write(welcome_mail.text)
                email_html.close()
                email_txt.close()
                msg_plain = render_to_string('welcome_email.txt',extra_args)
                msg_html = render_to_string('welcome_email.html', extra_args)
                subject = welcome_mail.subject
            send_mail(
            subject,
            msg_plain,
            'support@pharst.care',
            [email],
            html_message=msg_html,
            fail_silently=False,)