# from datetime import date, datetime, timedelta
# from decimal import Decimal
# from django.core.validators import FileExtensionValidator
# from dateutil import relativedelta
# from django.conf import settings
from datetime import datetime
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
# from django.contrib.postgres.fields import ArrayField
from django.db import models
# from django.db.models import Sum
# from django.urls import reverse
# from bonanza.fields import CountryField, CurrencyField
from django.utils import timezone
from django.utils.text import slugify
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField
import uuid
# from django.db.models import Q

# from pharstcare_web.fields import CountryField, CurrencyField

# Create your models here.

cascade_delete_rule = models.CASCADE
delete_rule = models.PROTECT

BASE_URL = "http://localhost:8070"

def generate_unique_id():
    # Generate a UUID and combine it with the current timestamp in milliseconds
    unique_id = f"{uuid.uuid4()}_{int(datetime.utcnow().timestamp() * 1000)}"
    return unique_id


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    deleted = models.DateTimeField(null=True, blank=True)
    uuid = models.CharField(max_length=255,default=generate_unique_id, editable=False, unique=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted = timezone.now()
        self.save()


class Region(TimeStamp):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=3, null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        db_table = "region"

    def __str__(self):
        return f"{self.name}"


class District(TimeStamp):
    name = models.CharField(max_length=255, null=False)
    code = models.CharField(max_length=5, null=True)
    region = models.ForeignKey(
        Region, related_name="district", on_delete=delete_rule, null=True
    )

    class Meta:
        db_table = "district"

    def __str__(self):
        return f"{self.name}"


class ActiveQuerySet(models.QuerySet):
    def only_active(self):
        return self.filter(
            deleted__isnull=True,
        )

    def delete(self):
        deleted_at = timezone.now()
        self.update(deleted=deleted_at)
        deleted, _rows_count = True, 0
        return deleted, _rows_count


# DJANGO ADMIN MODElS
class UserManager(BaseUserManager):
    def create_user(self, **other_fields):
        password = other_fields.pop("password", None)
        user = self.model(**other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, **other_fields):
        other_fields["is_superuser"] = True
        return self.create_user(**other_fields)


# Only to be used with the Django Admin application
class AdminUser(TimeStamp, PermissionsMixin, AbstractBaseUser):
    USERNAME_FIELD = "username"
    first_name = models.CharField(null=True, max_length=255,blank=True)
    last_name = models.CharField(null=True, max_length=255,blank=True)
    email = models.EmailField(null=True, blank=True)
    middle_name = models.CharField(null=True, max_length=255,blank=True)
    username = models.CharField(unique=True, db_index=True, max_length=255, null=True)
    password = models.CharField(null=False, max_length=500)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    new_password = models.CharField(null=True, max_length=500)
    date_joined = models.DateTimeField(auto_now_add=True,null=True)
    objects = UserManager()

    class Meta:
        db_table = "admin_user"

    def save(self, *args, **kwargs):
        if self.new_password:
            self.set_password(self.new_password)
            self.new_password = None

        return super().save(*args, **kwargs)


# PLATFORM USER MODElS
class Account(TimeStamp, AbstractBaseUser):
    objects = UserManager()
    MEMBER = "member"
    ADMIN = "admin"
    PROFESSIONAL_ASSOCIATE = "professional_associate"
    ACCOUNT_TYPES = Choices(
        (MEMBER, "member"),
        (PROFESSIONAL_ASSOCIATE, "professional_associate"),
        (ADMIN, "admin"),
    )
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_CHOICES = Choices(
        (
            GENDER_MALE,
            "Male",
        ),
        (
            GENDER_FEMALE,
            "Female",
        ),
    )

    ACTIVE = "active"
    DEACTIVATED = "deactivated"
    STATUS_CHOICES = ((ACTIVE, ACTIVE), (DEACTIVATED, DEACTIVATED))
    NORMAL_ASSOCIATE = "normal_associate"
    ADVANCED_ASSOCIATE = "advanced_associate"
    SUPER_ADMIN = "super_admin"
    CONTENT_MANAGER = "content_manager"
    GSET_MEMBER = "gset_member"
    PROFILES = Choices(
        (ADVANCED_ASSOCIATE,"Advanced Associate"),
        (NORMAL_ASSOCIATE,"Normal Associate"),
        (SUPER_ADMIN,"Super Admin"),
        (CONTENT_MANAGER,"Content Manager"),
        (GSET_MEMBER,"GSET Member"),
    )

    class Meta:
        verbose_name = "GSET User"
        verbose_name_plural = "GSET Users"
        db_table = "account"

    USERNAME_FIELD = "username"
    username = models.CharField(unique=True, db_index=True, max_length=255, null=True)
    first_name = models.CharField(null=True, max_length=255, blank=True)
    last_name = models.CharField(null=True, max_length=255, blank=True)
    middle_name = models.CharField(null=True, max_length=255, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, null=True,blank=True)
    email = models.EmailField(unique=True, db_index=True, null=True)
    phone_number = PhoneNumberField(null=True)
    user_img = models.ImageField(null=True, blank=True, upload_to="profile_photos")
    date_of_birth = models.DateField(null=True, blank=True)
    current_institution = models.CharField(null=True, max_length=255, blank=True)
    linkedin_profile = models.CharField(null=True, max_length=255, blank=True)
    short_bio = models.TextField(null=True,blank=True)
    region_of_institution = models.ForeignKey(Region,null=True, blank=True,on_delete=models.SET_NULL)
    account_type = models.CharField(
        choices=ACCOUNT_TYPES, default=MEMBER, max_length=25, null=True
    )
    password = models.CharField(null=True, max_length=500, blank=True)
    email_confirmed = models.BooleanField(default=False,null=True)
    phone_number_confirmed = models.BooleanField(default=False,null=True)
    reset_token = models.CharField(null=True, max_length=255, blank=True)
    login_attempts = models.IntegerField(default=0)
    must_reset_password = models.BooleanField(default=True)
    status = models.CharField(
        max_length=15, null=True, choices=STATUS_CHOICES, default=ACTIVE
    )
    date_joined = models.DateTimeField(null=True,blank=True,help_text="Date the user joined the platform.")
    slug = models.CharField(max_length=200, null=True)
    last_visit = models.DateTimeField(null=True,blank=True)
    last_login = models.DateTimeField(null=True,blank=True)
    current_profile = models.CharField(max_length=25,null=True,default=GSET_MEMBER,choices=PROFILES)
    professional_associations = models.JSONField(null=True,blank=True)
    resume = models.FileField(null=True, blank=True, upload_to="resumes")

    def __str__(self):
        return f"{self.id} {self.first_name} >> {self.email} :: {self.account_type}"
    
    def save(self, *args, **kwargs):
        if self.phone_number:
            self.slug = slugify(self.phone_number)
            self.referral_token = slugify(self.phone_number)
        return super().save(*args, **kwargs)
    


    

class Address(TimeStamp):
    user = models.OneToOneField(
        Account,
        null=True,
        on_delete=models.CASCADE,
        related_name="address",
        blank=False,
    )
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True, blank=True)
    digital_address = models.CharField(max_length=255, null=True, blank=True)
    address_line = models.CharField(max_length=255)
    zip = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "address"

    def __str__(self):
        if hasattr(self,"account"):
            return f"address for {self.account.phone_number}"
        return "Address with no user"

class PersonalSettings(TimeStamp):
    user = models.OneToOneField(
        Account,
        null=True,
        on_delete=models.CASCADE,
        related_name="settings",
        blank=False,
    )
    sms_notifications = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=False)
    in_app_notifications = models.BooleanField(default=True)
    whatsapp_notifications = models.BooleanField(default=False)
    whatsapp_phone = PhoneNumberField(unique=False, null=True)
    active_phone = PhoneNumberField(unique=False, null=True)

    class Meta:
        db_table = "personal_settings"

    def __str__(self):
        if self.user:
            return f"settings for {self.user.phone_number}"
        return "Settings with no user"




class VerificationCode(TimeStamp):
    CHANGE_EMAIL = "change_email"
    CHANGE_PHONE_NUMBER = "change_phone_number"
    FORGOT_PASSWORD = "forgot_password"
    LOGIN = "login"
    CREATE_ACCOUNT = "create_account"
    VERIFICATION_ACTIONS = Choices(
        (CHANGE_EMAIL, "Change email"),
        (CHANGE_PHONE_NUMBER, "Change Phone number"),
        (FORGOT_PASSWORD, "Forgot password"),
        (LOGIN, "Login"),
        (CREATE_ACCOUNT, "Create Account"),
    )

    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    WHATSAPP = "whatsapp"
    VERIFICATION_TYPES = Choices(
        (EMAIL, "Email"),
        (PHONE_NUMBER, "Phone number"),
        (WHATSAPP, "WhatsApp"),
    )

    verification_type = models.CharField(
        null=True, choices=VERIFICATION_TYPES, max_length=35
    )
    verification_action = models.CharField(
        null=True, choices=VERIFICATION_ACTIONS, max_length=35
    )
    account = models.ForeignKey(Account, null=True, on_delete=cascade_delete_rule)
    email = models.EmailField(null=True)
    phone_number = PhoneNumberField(null=True)
    whatsapp_phone = PhoneNumberField(null=True)
    code = models.CharField(null=False, max_length=255)
    expiry = models.DateTimeField(null=True)
    status = models.CharField(
        choices=[("verified", "Verified")], null=True, max_length=25
    )

    class Meta:
        db_table = "verification_code"

    def __str__(self):
        return f"{self.verification_type}: {self.email or self.phone_number or ''}"
    

class BGTask(TimeStamp):
    TASK_STATUSES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]

    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    name = models.CharField(max_length=255)  # Task function name
    args = models.JSONField()  # Arguments for the task function
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default='pending')  # Task status
    execution_time = models.DateTimeField(default=timezone.now)  # Time when the task should be executed
    retries = models.IntegerField(default=0)  # Retry count
    max_retries = models.IntegerField(default=3)  # Max retries
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')  # Task priority
    log = models.TextField(blank=True,null=True)  # Log for task execution details
    result = models.JSONField(null=True)

    def __str__(self):
        return f"BGTask: {self.name}, Status: {self.status}, Priority: {self.priority}"
    
    class Meta:
        db_table = "bg_task"


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=200,default='Pharst Newsletter')
    text = models.TextField(null=True,blank=True)
    body = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = "email_template"


class Image(TimeStamp):
    image = models.ImageField(upload_to="course_contents")

    def __str__(self):
        return f"{BASE_URL}{self.image.url}"

    class Meta:
        db_table = "image"


class Course(TimeStamp):
    name = models.CharField(max_length=255,null=True,blank=True)
    instructor = models.ForeignKey(Account,null=True,on_delete=models.SET_NULL)
    description = models.TextField(null=True)
    cover_image = models.ImageField(null=True,upload_to="courses")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "course"


class Chapter(TimeStamp):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,related_name="chapters")
    title = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField(null=True)
    position = models.IntegerField(null=True)
    cover_image = models.ImageField(null=True,upload_to="courses")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "chapter"

    