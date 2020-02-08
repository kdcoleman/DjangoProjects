from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('confirm/<slug:uid64>/<slug:token>/', views.confirm, name='confirm'),
    path('<int:user_id>/home/', login_required(views.home), name='home'),
]
