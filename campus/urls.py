"""campus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^register/', user_views.register, name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', user_views.activate, name='activate'),  
    url(r'^profile/', user_views.profile, name='profile'),
    url(r'^login/', user_views.student_login_request, name='login'),
    url(r'^pcell_login/', user_views.pcell_login_request, name='pcell_login'),
    url(r'^logout/', user_views.logout_request, name='logout'),
    url(r'^show_offers/', user_views.show_users, name='show_offers'),
    url(r'^delete_user/(?P<username>[\w|\W.-]+)/$', user_views.delete_user, name='delete_user'),
    url(r'^', include('placement.urls')),
    url(r'^', include('pcell.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
