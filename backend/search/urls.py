from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search),
    path('detail', views.detail),
    path('autoComplete', views.autoComplete)
]
