from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search),
    path('submitEntry', views.submitEntry),
    path('reportEntry', views.reportEntry),
    path('detail', views.detail),
    path('autoComplete', views.autoComplete)
]
