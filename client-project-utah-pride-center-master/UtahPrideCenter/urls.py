from django.urls import path
from . import views

urlpatterns = [
    # landing page
    path('', views.index, name='index'),

    # check in form
    path('CheckIn/', views.check_in, name='CheckIn'),

    # edit user info
    path('EditInfo/', views.edit_info, name='EditInfo'),

    # confirm check in
    path('Confirmation/', views.confirmation, name='Confirmation'),

    path('update/', views.update, name='update'),
]