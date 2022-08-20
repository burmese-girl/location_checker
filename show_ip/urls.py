from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('dashboard/', views.LocationListView.as_view(), name='dashboard'),
    path('pie_chart/', views.pie_chart, name='pie_chart'),
    path('heap_map/', views.heap_map, name='heap_map'),
]
