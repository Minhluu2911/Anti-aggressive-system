from django.urls import URLPattern, path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'register'

urlpatterns = [
    path('register', views.register, name = "register"),
    path('register_request', views.register_request, name = "register_request"),
    path('login', views.login_request, name = "login"),
    path('logout', views.logout_request, name = "logout"),
    # path('homepage_user', views.homepage_user),
    # path('homepage_admin', views.homepage_admin),
   # path('accounts/', include('django.contrib.auth.urls')),

    #for password reset, not done yet
    path('password_reset', views.password_reset_request, name = "password_reset_request"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='register/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="register/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='register/password/password_reset_complete.html'), name='password_reset_complete'),      

    path('accounts/', include('allauth.urls'), name = "accounts"),
]
    