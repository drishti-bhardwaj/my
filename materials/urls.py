from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/cpses/', views.api_cpses, name='api_cpses'),
    path('api/cpses/<str:cpse_id>/', views.api_cpse_detail, name='api_cpse_detail'),
]
