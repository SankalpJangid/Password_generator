from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login_1, name='login'),
    path('', views.home, name='home'),
    path('logout', views.logout_user, name= "logout_user"),
    path('registration', views.registration, name='registration'),
    path('login_user', views.login_user, name="login_user"),
    path('generate', views.generate, name="generate"),
    path('save_password', views.save_passwords, name="save_password"),
    path('delete/<int:id>', views.delete_pass, name="delete/<int:id>"),
    path('update/<int:id>', views.update_pass, name="update/<int:id>"),
    path('sample', views.sample_model, name="sample"),
    path('check', views.check, name="check"),
    path('change',views.change_data, name="change"),
    path('search', views.search, name="search"),
]