from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^show_company/$', views.show_company, name='show_company'),
<<<<<<< HEAD
    url(r'add_company', views.add_company, name='WWadd_company'),
=======
    url(r'add_company', views.add_company, name='add_company'),
>>>>>>> 7300511f230011326a14e87745ac78a367ec76e3
    url(r'^announcement/$', views.announcement, name='announcement'),
    url(r'^add_announcement/$', views.add_announcement, name="add_announcement"),
    path('add_stats', views.add_stats, name="add_stats"),
    url(r'^your_app/$', views.your_app, name='your_app'),
    path('show_description/<int:company_id>',
         views.show_description, name='show_description'),
    path('apply_job/<int:company_id>', views.apply_job, name='apply_job'),
    url(r'^show_campus/$', views.show_campus, name='show_campus'),
]
