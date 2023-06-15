from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registrationPage, name="register"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('change-password/<id>/', views.change_password, name='change_password')


]
