from datetime import datetime, timedelta
from django.utils import timezone
from api.client_api.auth.utils import Base64FileField, get_user_wallet
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from drf_extra_fields.fields import Base64ImageField

from api.utils import CheckPasswordValidity, generate_token, get_object_or_404_with_error
from core.models import Account, Address, PersonalSettings, VerificationCode

LOGIN_ATTEMPTS_THRESHOLD = 2

class PersonalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalSettings
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        ref_name = "address"
        fields = (
            "id",
            "created",
            "country",
            "address_line",
            "city",
            "state",
            "digital_address",
            "zip",
        )



class AccountSerializer(serializers.ModelSerializer):
    user_img = Base64ImageField(required=False, allow_null=True)
    resume = Base64FileField(required=False, allow_null=True)
    class Meta:
        model = Account
        ref_name = "account"
        fields = "__all__"

    def to_representation(self,instance):
        data = super().to_representation(instance)
        data["address"] = None
        data["settings"] = None
        if hasattr(instance,"address"):
            data["address"] = AddressSerializer(instance.address).data
        if hasattr(instance,"settings"):
            data["settings"] = PersonalSettingsSerializer(instance.settings).data
        if instance.region_of_institution:
            data["region_of_institution_name"] = instance.region_of_institution.name 
        return data




class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        ref_name = "client"

    def validate(self, data):
        validated_data = super().validate(data)
        email = validated_data.pop("email", None)
        password = validated_data.pop("password", None)

        if email is not None:
            if not Account.objects.filter(email=email).exists():
                account = get_object_or_404_with_error(
                    "Account not found!", Account, email=email
                )
            else:
                account = Account.objects.get(email=email)
            if account.login_attempts > LOGIN_ATTEMPTS_THRESHOLD:
                raise serializers.ValidationError(
                    "Too many attempts, please request for password reset."
                )
            validated_data["email"] = account.email
            if account.account_type != Account.MEMBER:
                raise serializers.ValidationError(
                    "Admins not permitted to use the Client Portal"
                )

            if not account.check_password(password):
                # if attempts higher than the allowed, we lock any other attempts
                # increase attempt
                account.login_attempts += 1
                account.save()
                raise serializers.ValidationError("Incorrect password entered")
        return validated_data

    def save(self):
        email = self.validated_data["email"]
        self.validated_data["user"] = Account.objects.get(email=email)
        return self.validated_data


class CheckPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    country = serializers.CharField(required=True)

    class Meta:
        ref_name = "client-check-phone-exists"

    def validate(self, data):
        validated_data = super().validate(data)
        phone_number = validated_data.get("phone_number")
        country = validated_data.get("country")
        # is the country among our list of allowed countries?
        allowed_countries = ["Ghana","Nigeria"]
        if country not in allowed_countries:
            raise serializers.ValidationError(
                    "Pharstcare operates in: ".join([i for i in allowed_countries])
                )
        # does the user exist
        if phone_number is not None:
            if not Account.objects.filter(phone_number=phone_number).exists():
                validated_data["user_exists"] = False
            else:
                account = Account.objects.get(phone_number=phone_number)
                validated_data["user_exists"] = True
                validated_data["user"] = account
        return validated_data

    def save(self):
        phone_number = self.validated_data["phone_number"]
        if not self.validated_data.get("user_exists"):
            # create an account for user if they don't have one already
            account_data = {"phone_number":phone_number,"username":phone_number,"date_joined":timezone.now()}
            account = Account.objects.create(**account_data)
            # create an address
            address_data = {
                "country":self.validated_data["country"],
                "user":account
            }
            Address.objects.create(**address_data)
            # create settings
            settings_data = {
                "in_app_notifications":True,
                "user":account
            }
            PersonalSettings.objects.create(**settings_data)
            self.validated_data["user"] = account
        else:
            account = self.validated_data["user"]
            # does the person have settings and address?
            if not hasattr(account,"address"):
                # create an address
                address_data = {
                    "country":self.validated_data["country"],
                    "user":account
                }
                Address.objects.create(**address_data)
            if not hasattr(account,"settings"):
                # create settings
                settings_data = {
                    "in_app_notifications":True,
                    "user":account
                }
                PersonalSettings.objects.create(**settings_data)
        return self.validated_data


class CompletSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    notification_token = serializers.CharField(required=False)

    class Meta:
        ref_name = "client-complete-signup"

    def validate(self, data):
        validated_data = super().validate(data)
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = self.context["request"].user
        # we can't have the same email already in the system
        if email and Account.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email address is already taken")
        if not CheckPasswordValidity(password):
            raise serializers.ValidationError("Create a more secure password")
        validated_data["user"] = user
        return validated_data

    def save(self):
        user = self.validated_data["user"]
        email = self.validated_data["email"]
        notification_token = self.validated_data.get("notification_token")
        password = self.validated_data["password"]
        user.set_password(password)
        # now set email and notification fields
        user.email = email
        user.pharst_fcm_token = notification_token
        user.phone_number_confirmed = True
        user.save()
        self.validated_data["user"] = user
        return self.validated_data
    

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        ref_name = "client-signup"

    def validate(self, data):
        validated_data = super().validate(data)
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = self.context["request"].user
        # we can't have the same email already in the system
        if email and Account.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email address is already taken")
        if not CheckPasswordValidity(password):
            raise serializers.ValidationError("Create a more secure password")
        validated_data["user"] = user
        return validated_data

    def save(self):
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        # create user
        user = Account(email=email)
        user.set_password(password)
        user.save()
        self.validated_data["user"] = user
        return self.validated_data


class SendVerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = [
            "id",
            "created",
            "email",
            "phone_number",
            "whatsapp_phone",
            "account",
            "verification_type",
            "verification_action",
        ]

    def validate(self, data):
        validated_data = super().validate(data)
        email = validated_data.get("email")
        phone_number = validated_data.get("phone_number")
        whatsapp_phone = validated_data.get("whatsapp_phone")
        verification_type = validated_data.get("verification_type")
        if not email and verification_type == VerificationCode.EMAIL:
            raise serializers.ValidationError("Email required")
        if not phone_number and verification_type == VerificationCode.PHONE_NUMBER:
            raise serializers.ValidationError("Phone required")
        if not whatsapp_phone and verification_type == VerificationCode.WHATSAPP:
            raise serializers.ValidationError("Whatsapp Phone required")
        code = generate_token(4)
        validated_data["code"] = code
        validated_data["expiry"] = timezone.now() + timedelta(minutes=10)
        return validated_data


class VerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = [
            "id",
            "created",
            "email",
            "phone_number",
            "account",
            "verification_action",
            "verification_type",
            "code",
        ]

    def validate(self, data):
        validated_data = super().validate(data)

        verification_code = VerificationCode.objects.filter(
            **validated_data, status__isnull=True
        ).last()

        if not verification_code:
            raise serializers.ValidationError("Code is not valid")

        if verification_code.expiry and verification_code.expiry <= timezone.now():
            raise serializers.ValidationError("Code has expired")

        if (
            verification_code.verification_action
            == VerificationCode.VERIFICATION_ACTIONS.change_phone_number
            and Account.objects.exclude(id=verification_code.account.id)
            .filter(phone_number=verification_code.phone_number)
            .exists()
        ):
            raise serializers.ValidationError(
                "Account with this phone number already exists"
            )

        if (
            verification_code.verification_action
            == VerificationCode.VERIFICATION_ACTIONS.change_email
            and Account.objects.exclude(id=verification_code.account.id)
            .filter(email=verification_code.email)
            .exists()
        ):
            raise serializers.ValidationError("Account with this email already exists")

        return validated_data

    def save(self):
        return VerificationCode.objects.filter(
            **self.validated_data, status__isnull=True
        ).last()


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    class Meta:
        ref_name = "client"

    def validate(self, data):
        validated_data = super().validate(data)
        phone_number = validated_data.get("phone_number")

        if (
            phone_number
            and not Account.objects.filter(phone_number=phone_number).exists()
        ):
            raise serializers.ValidationError(
                "No account exists with the given phone number"
            )

        return validated_data

    def save(self):
        phone_number = self.validated_data["phone_number"]
        account = Account.objects.get(phone_number=phone_number)
        self.validated_data["account"] = account
        return self.validated_data


class ResendVerificationSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    whatsapp_phone = serializers.CharField(required=False)
    verification_type = serializers.CharField(required=True)

    class Meta:
        ref_name = "client"

    def validate(self, data):
        validated_data = super().validate(data)
        id_ = validated_data.get("id")
        verification_type = validated_data.get("verification_type")
        if verification_type == VerificationCode.PHONE_NUMBER and (id_ and not Account.objects.filter(phone_number=id_).exists()):
                raise serializers.ValidationError(
                    "No account exists with the given phone number"
                )
        if verification_type == VerificationCode.EMAIL and (id_ and not Account.objects.filter(email=id_).exists()):
                raise serializers.ValidationError(
                    "No account exists with the given email"
                )
        if verification_type == VerificationCode.WHATSAPP and (id_ and not Account.objects.filter(phone_number=id_).exists()):
                raise serializers.ValidationError(
                    "No account exists with the given phone number"
                )

        return validated_data

    def save(self):
        verification_type = self.validated_data["verification_type"]
        id_ = self.validated_data["id"]
        if verification_type in [VerificationCode.PHONE_NUMBER,VerificationCode.WHATSAPP]:
            self.validated_data["account"] = Account.objects.get(phone_number=id_)
        if verification_type == "email":
            self.validated_data["account"] = Account.objects.get(email=id_)
        return self.validated_data


class VerifyForgotPasswordLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = [
            "id",
            "created",
            "email",
            "phone_number",
            "account",
            "verification_action",
            "verification_type",
            "code",
        ]

    def validate(self, data):
        validated_data = super().validate(data)

        verification_code = VerificationCode.objects.filter(
            **validated_data, status__isnull=True
        ).last()

        if not verification_code:
            raise serializers.ValidationError("Code is not valid")

        if verification_code.expiry and verification_code.expiry <= timezone.now():
            raise serializers.ValidationError("Code has expired")

        if (
            verification_code.verification_action == VerificationCode.PHONE_NUMBER
            and Account.objects.exclude(id=verification_code.account.id)
            .filter(phone_number=verification_code.phone_number)
            .exists()
        ):
            raise serializers.ValidationError(
                "Account with this phone number already exists"
            )

        if (
            verification_code.verification_action
            == VerificationCode.VERIFICATION_ACTIONS.change_email
            and Account.objects.exclude(id=verification_code.account.id)
            .filter(email=verification_code.email)
            .exists()
        ):
            raise serializers.ValidationError("Account with this email already exists")

        return validated_data

    def save(self):
        return VerificationCode.objects.filter(
            **self.validated_data, status__isnull=True
        ).last()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        ref_name = "clinet_change_password"

    def validate(self, data):
        validated_data = super().validate(data)
        user = self.context["request"].user
        old_password = validated_data["old_password"]
        new_password = validated_data["new_password"]
        if not check_password(old_password, user.password):
            raise serializers.ValidationError("Password entered is incorrect")
        if old_password == new_password:
            raise serializers.ValidationError("New password cannot be same as old")
        validated_data["user"] = user
        return validated_data