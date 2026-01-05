from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginView.as_view(),name='login'),
    path('token/refresh/',TokenRefreshView.as_view(),name='refresh'),
    path('list-create/task/',CreateListTaskView.as_view(),name='task'),
    path('get/update/delete/<uuid:pk>/',RetrieveUpdataeDeleteView.as_view(),name="nothing"),
]