from django.urls import path
from . import views

urlpatterns = [
    path('', views.nl2sql_query_view, name='nl2sql_query'),
]