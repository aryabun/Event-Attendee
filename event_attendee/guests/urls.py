from django.urls import path
from . import views

urlpatterns = [
    path('guest/', views.check_validate),
    path('admin/', views.admin_page_view, name='admin'),
    path('guest_list/', views.guests_list_view),
]