from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('profile/', views.profile , name='profile'),
    path('register/', views.register , name='register'),
    path('create/', views.create_design_request, name='create'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('request/<int:request_id>/delete/', views.delete_design_request, name='delete_request'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/categories/', views.categories_list, name='categories_list'),
    path('admin-panel/categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('admin-panel/status/', views.filter_status, name='filter_status'),
    path('admin-panel/status/<int:request_id>/', views.update_status, name='update_status'),
]


