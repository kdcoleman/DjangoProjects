from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/home/', login_required(views.home), name='home'),
]
