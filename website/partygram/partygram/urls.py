"""partygram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from main import views
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('welcome', views.welcome, name='welcome'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name = "signup"),
    path('profile/', views.profile, name = 'profile'),
    path('upload_avatar', views.upload_avatar, name='upload_avatar'),
    path('upload_identification', views.upload_identification, name="upload_identification"),
    path('upload_moment/', views.upload_moment, name = 'upload_moment')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)