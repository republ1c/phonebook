from django.urls import path
from .views import *
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', phonebook_list, name='phonebook_list'),
    path('', RedirectView.as_view(url='/phonebook'), name='phonebook'),
    path('update/<int:pk>/', UserUpdate.as_view(), name='user_update_url'),
    path('delete/<int:pk>/', UserDelete.as_view(), name='user_delete_url'),
    # path('update/<int:pk>/', UserUpdate.as_view(), name='user_update_url'),
    path('create/', UserCreate.as_view(), name='user_create_url')

]
