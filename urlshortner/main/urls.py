from django.urls import path, re_path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="registerset"),
    path("get_token/", views.get_token, name="token"),
    path("url/", views.generate_url, name="generate_url"),
    path("geturl/", views.get_url, name="geturl"),
    path("all_urls/", views.get_all_urls, name="all_urls"),
    re_path(r"^(?P<short_url>[a-zA-z0-9]+)/", views.go_to_url, name="go_url"),
]
