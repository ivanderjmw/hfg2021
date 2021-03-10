from django.urls.conf import path, re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.landing, name='landing')  # if matches raw empty string
]
