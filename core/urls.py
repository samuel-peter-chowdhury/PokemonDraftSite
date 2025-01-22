"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from users import views as user_views
from django.conf import settings
from django.views.static import serve
from django.contrib.auth import views as auth_views
#from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    re_path(r'^(?P<id>\w+)/password/$', user_views.change_password_view, name='change_password'),
    path('leagues/', include('leagues.urls')),
    path('pokemons/', include('pokemons.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "users/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "users/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "users/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "users/password_reset_done.html"), name ='password_reset_complete'),
]

# Debug settings
# urlpatterns = [
#     re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
#     re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
#     path('admin/', admin.site.urls),
#     path('', views.homepage),
#     path('users/', include('users.urls')),
#     path('users/', include('django.contrib.auth.urls')),
#     re_path(r'^(?P<id>\w+)/password/$', user_views.change_password_view, name='change_password'),
#     path('leagues/', include('leagues.urls')),
#     path('pokemons/', include('pokemons.urls')),
#     path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "users/reset_password.html"), name ='reset_password'),
#     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "users/password_reset_sent.html"), name ='password_reset_done'),
#     path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "users/password_reset_form.html"), name ='password_reset_confirm'),
#     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "users/password_reset_done.html"), name ='password_reset_complete'),
# ] + debug_toolbar_urls()
