from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path(r'^$',views.index),
    re_path(r'^signup/$',views.register),
    re_path(r'^login/$',views.login),
    re_path(r'^member-dashboard/$',views.dashboard_profile),
    re_path(r'^member-courses/$',views.dashboard_courses),
    re_path(r'^member-chapter/(?P<id>[-\w]+)/$',views.dashboard_course),
    re_path(r'^member-jobs/$',views.dashboard_jobs),
    re_path(r'^jobs/(?P<id>[-\w]+)/$',views.job),

]