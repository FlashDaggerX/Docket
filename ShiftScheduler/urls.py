"""ShiftScheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

import calender.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.make_welcome, name='index'),
    path('event/<int:id>', views.update_event, name='update_event'),
    path('event/new', views.new_event, name='new_event'),
    path('event/delete/<int:id>', views.delete_event, name='delete_event'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/new', views.new_user, name='new_user'),
    path('shifts/', views.make_shifts, name='view_shifts'),
]
