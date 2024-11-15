"""gsetpa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.views.static import serve
import debug_toolbar
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("frontend.urls")),
    path("api/", include("api.urls")),
    path("health", lambda x: HttpResponse("ok"), name="health"),
    path("__debug__/", include(debug_toolbar.urls)),
    path('oauth/', include('social_django.urls', namespace='social')),
]

urlpatterns += [
        path(f'{settings.MEDIA_URL.lstrip("/")}<path:path>/', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]