from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_views

from api import views 


urlpatterns = [
    url(r'^api/login', views.login),
    url(r'^api/logout', views.logout),
    url(r'^api/accounts/', include('django.contrib.auth.urls')),
    url(r'^api/profiles$', views.user_list),
    url(r'^api/profiles/(?P<id>[0-9]{1,})$', views.user_details),
    url(r'^api/schools$', views.school_list),
    url(r'^api/schools/(?P<id>[0-9]{1,})$', views.school_detail),
    url(r'^api/schools/changeMode/(?P<id>[0-9]{1,})$',views.school_change_mode),
    url(r'^api/students/list/(?P<schoolid>[0-9]{1,})$', views.student_list),
    url(r'^api/students/details/(?P<id>[0-9]{1,})$', views.student_details),
    url(r'^api/observations/list/(?P<id_student>[0-9]{1,})$', views.observation_list),
    url(r'^api/observations/details/(?P<id_observation>[0-9]{1,})$', views.observation_detail),
    url(r'^api/subscriptions/(?P<school_id>[0-9]{1,})$', views.subscription_detail),
    url(r'^api/transfers$', views.transfer_list),
]