from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('search', views.search),
    path('searchEntry', views.searchEntry),
    path('reportEntry', views.reportEntry),
    path('detail', views.detail),
    path('autoComplete', views.autoComplete),
    path('getEntry', views.getEntry),
    path('deleteEntry', views.deleteEntry),
    path('getAllEntries', views.getAllEntries),
    path('getAllReviews', views.getAllReviews),
    path('updateEntry', views.updateEntry),
    path('denyReview', views.denyReview)
]
