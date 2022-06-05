
from django.urls import path
from . import views

app_name='style_transfer'

urlpatterns = [

    path('', views.MainView.as_view(), name='index'),
]
