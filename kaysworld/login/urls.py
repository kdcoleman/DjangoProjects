from django.urls import path

from . import views

app_name = 'login'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('confirm/<slug:uid64>/<slug:token>/', views.confirm, name='confirm'),
    path('extend/', views.extend_session, name='extend'),
    path('expire/', views.expire_session, name='expire'),
    path('<int:user_id>/home/', views.home, name='home'),
]
