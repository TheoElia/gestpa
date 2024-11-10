from datetime import datetime
from django.utils import timezone
from rest_framework import mixins, response, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from api.client_api.auth.permissions import LoginPermission, ProfilePermission #, ProfilePermission
from api.client_api.auth.serializers import (
    AccountSerializer,
    ChangePasswordSerializer,
    CheckPhoneSerializer,
    CompletSignupSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    ResendVerificationSerializer,
    SendVerificationCodeSerializer,
    SignupSerializer,
    VerifyCodeSerializer,
    VerifyForgotPasswordLinkSerializer,
)
from api.utils import getLoginToken
from core.models import Account, VerificationCode
from utils.emails.send import EmailNotification
from utils.sms.send import SMSNotification
from utils.sms.templates import SMSTemplate
from utils.whatsapp.send import WhatsappNotification


template = SMSTemplate()
sms_notification = SMSNotification()
email_notification = EmailNotification()
whatsapp_notification = WhatsappNotification()

class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=CheckPhoneSerializer,
        permission_classes=[AllowAny],
    )
    def check_phone_exists(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        user = result["user"]
        code = None
        if user.phone_number_confirmed is not True:
            # send sms
            serializer = SendVerificationCodeSerializer(
            data={
                "account": user.pk,
                "phone_number": str(user.phone_number),
                "verification_type": VerificationCode.PHONE_NUMBER,
                "verification_action": VerificationCode.CREATE_ACCOUNT,
            },
                context=self.get_serializer_context(),
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(account=user)
            validated_data = serializer.validated_data
            code = validated_data["code"]
            welcome_sms = template.welcome(code)
            payload = {
                "phone":[str(user.phone_number)],
                "body":welcome_sms
            }
            sms_notification.send_sms(payload)
        # get client using secret code
        token = getLoginToken(user)
        user_data = AccountSerializer(user).data
        # DISCUSS: should we include the code, could cause a security breach.
        # user_data["code"] = code
        data = {
            "success":True,
            "message":"Account create/retrieved for user",
            "user":user_data
        }
        return response.Response(
            data,
            headers={
                "set-auth-token": str(token.access_token),
                "set-refresh-token": str(token),
            },
        )
    
    @action(
        methods=["POST"],
        detail=False,
        serializer_class=SignupSerializer,
        permission_classes=[AllowAny],
    )
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        user = result["user"]
        token = getLoginToken(user)
        user_data = AccountSerializer(user).data
        data = {
            "success":True,
            "message":"Signup completed",
            "user":user_data
        }
        return response.Response(
            data,
            headers={
                "set-auth-token": str(token.access_token),
                "set-refresh-token": str(token),
            },
        )

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=CompletSignupSerializer,
        permission_classes=[LoginPermission],
    )
    def complete_signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        user = result["user"]
        token = getLoginToken(user)
        user_data = AccountSerializer(user).data
        data = {
            "success":True,
            "message":"Signup completed",
            "user":user_data
        }
        return response.Response(
            data,
            headers={
                "set-auth-token": str(token.access_token),
                "set-refresh-token": str(token),
            },
        )

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=LoginSerializer,
        permission_classes=[AllowAny],
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        user = result["user"]
        # if user.phone_number_confirmed is not True:
        #     user.phone_number_confirmed = True
        # get client using secret code
        token = getLoginToken(user)
        user.last_login = timezone.now()
        user.last_visit = timezone.now()
        user.save()
        user_data = AccountSerializer(user).data
        data = {
            "success":True,
            "message":"Logged in successgfully",
            "user":user_data
        }
        return response.Response(
            data,
            headers={
                "set-auth-token": str(token.access_token),
                "set-refresh-token": str(token),
            },
        )

    @action(methods=["GET"], detail=False, permission_classes=[LoginPermission])
    def refresh(self, request):
        user = request.user
        token = getLoginToken(user)
        return response.Response(
            {"success": True},
            headers={
                "set-auth-token": str(token.access_token),
                "set-refresh-token": str(token),
            },
        )

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=VerifyCodeSerializer,
        permission_classes=[LoginPermission],
    )
    def verify_phone_number(self, request):
        user = request.user
        serializer = self.get_serializer(
            data={
                **request.data,
                "user": user.pk,
                "verification_type": VerificationCode.PHONE_NUMBER,
                "verification_action": VerificationCode.CREATE_ACCOUNT,
            },
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        verification = serializer.save()
        user.phone_number = verification.phone_number
        user.phone_number_confirmed = True
        user.save()
        return response.Response({"success": True})

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=ResendVerificationSerializer,
        permission_classes=[AllowAny],
    )
    def resend_verification_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        user = result.get("account")
        verification_type = result.get("verification_type")
        # determine if the person is using email, whatsapp or phone number
        code_data = {
                "account": user.pk,
                "verification_type": verification_type,
                "verification_action": VerificationCode.CREATE_ACCOUNT,
            }
        if verification_type == VerificationCode.PHONE_NUMBER:
            code_data["phone_number"] = str(user.phone_number)
        if verification_type == VerificationCode.EMAIL:
            code_data["email"] = user.email
        if verification_type == VerificationCode.WHATSAPP:
            code_data["whatsapp_phone"] = result.get("whatsapp_phone")
        serializer = SendVerificationCodeSerializer(
            data=code_data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(account=user)
        validated_data = serializer.validated_data
        # depending on the type we send
        code = validated_data["code"]
        if verification_type == VerificationCode.PHONE_NUMBER:
            welcome_sms = template.welcome(code)
            payload = {
                "phone":[str(user.phone_number)],
                "body":welcome_sms
            }
            sms_notification.send_sms(payload)
        if verification_type == VerificationCode.EMAIL:
            email = user.email
            email_subject = "Welcome To Pharstcare"
            extra_args = {
                "user":user,
                "code":code
            }
            email_notification.email_users_only_emails(emails=[email],email_subject=email_subject,extra_args=extra_args)

        if verification_type == VerificationCode.WHATSAPP:
            payload = {
                "phones":[result.get("whatsapp_phone")],
                "code":code
            }
            whatsapp_notification.send_otp_whatsapp_message(payload)

        # send_sms_verification_code(
        #     validated_data["account"],
        #     validated_data["phone_number"],
        #     validated_data["code"],
        # )
        token = getLoginToken(user)
        return response.Response(
            {"success": True, "message": f"Code sent to {code_data.get('verification_type')}","Code":code},
            headers={
                "set-auth-token": str(token.access_token),
                "set-refresh-token": str(token),
            },
        )

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=ForgotPasswordSerializer,
        permission_classes=[],
    )
    def forgot_password(self, request):
        serializer = self.get_serializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        account = result["account"]
        serializer = SendVerificationCodeSerializer(
            data={
                "account": account.pk,
                "phone_number": str(account.phone_number),
                "verification_type": VerificationCode.PHONE_NUMBER,
                "verification_action": VerificationCode.FORGOT_PASSWORD,
            },
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(account=account)
        validated_data = serializer.validated_data

        # send_sms_verification_code(
        #     validated_data["account"],
        #     validated_data["phone_number"],
        #     validated_data["code"],
        # )
        code = validated_data["code"]
        token = getLoginToken(account)
        return response.Response(
            {"success": True, "message": "Reset password code sent!", "code": code},
            headers={
                "set-auth-token": str(token.access_token),
                "set-refresh-token": str(token),
            },
        )

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=VerifyForgotPasswordLinkSerializer,
        permission_classes=[LoginPermission],
    )
    def reset_password(self, request):
        serializer = self.get_serializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        user = request.user
        password = request.data["password"]
        serializer = VerifyCodeSerializer(
            data={
                **request.data,
                "user": user.pk,
                "verification_type": VerificationCode.PHONE_NUMBER,
                "verification_action": VerificationCode.FORGOT_PASSWORD,
            },
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        verification = serializer.save()
        user = verification.account
        user.set_password(password)
        user.save()
        return response.Response(
            {"success": True, "message": "Password reset successful"}
        )

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=ChangePasswordSerializer,
        permission_classes=[LoginPermission],
    )
    def change_password(self, request):
        serializer = self.get_serializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.must_reset_password = False
        password = serializer.validated_data["new_password"]
        user.set_password(password)
        user.save()
        return response.Response({"success": True})




class ProfileViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [LoginPermission, ProfilePermission]

    def get_object(self):
        return self.request.user

    @action(methods=["GET"], detail=False,permission_classes=[LoginPermission,])
    def self(self, request):
        client = request.user
        return response.Response(AccountSerializer(client).data)

    def partial_update(self, request, *args, **kwargs):
        update_response = super().partial_update(
            request,
            *args,
            **kwargs,
        )
        return update_response