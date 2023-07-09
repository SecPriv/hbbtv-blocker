from django.urls import include, re_path

from . import views

urlpatterns = [
    re_path('blocklist', views.blocklist, name='blocklist'),
    re_path('about', views.about, name='about'),
    re_path('', views.index, name='index')
]
