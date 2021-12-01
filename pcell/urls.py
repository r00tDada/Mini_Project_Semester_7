from django.conf.urls import url
from pcell import views
from django.urls import path


urlpatterns = [
   url(r'^pcell_index/$', views.pcell_index, name='pcell_index'),
   url(r'^pcell_show_campus/$', views.pcell_show_campus, name='pcell_show_campus'),
#   url(r'^pcell_add_stats/$', views.pcell_add_stats, name='pcell_add_stats'),
   url(r'^pcell_show_company/$', views.pcell_show_company, name='pcell_show_company'),
   path('pcell_show_description/<int:company_id>',
         views.pcell_show_description, name='pcell_show_description'),
   url(r'^pcell_company_view/$', views.pcell_company_view, name='pcell_company_view'),
   url(r'^pcell_announcement/$', views.pcell_announcement, name='pcell_announcement'), 
   url(r'^pcell_add_company/', views.pcell_add_company, name='pcell_add_company'),
   url(r'^pcell_add_announcement/$', views.pcell_add_announcement, name="pcell_add_announcement"),
   url(r'pcell_add_stats/$', views.pcell_add_stats, name="pcell_add_stats"),
]
