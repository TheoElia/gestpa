from django.contrib import admin
from django.contrib.admin import register
from .forms import ChapterCreationForm,ChapterChangeForm

from core.models import Account, AdminUser, Chapter, Course, Image
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    add_form = ChapterCreationForm
    form = ChapterChangeForm


@register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    readonly_fields = ("password","is_superuser")


@register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass