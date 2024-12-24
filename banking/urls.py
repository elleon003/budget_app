from django.urls import path
from . import views

app_name = 'banking'

urlpatterns = [
    path('accounts/', views.account_list, name='accounts'),
]
