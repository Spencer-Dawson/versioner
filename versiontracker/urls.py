from django.urls import path

from . import views
from . import api

urlpatterns = [
    path('api', views.ApiView),
    path('api/AppVersion', views.ApiAppVersionView),
    path('api/AppEnvironment', views.ApiAppEnvironmentView),
    path('api/AppName', views.ApiAppNameView),
    path('api/AppHistory', views.ApiAppHistoryView),
    path('api/AppCurrentDeploys', views.ApiAppCurrentDeploysView),
    path('', views.index),
]
