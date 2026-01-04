from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginView.as_view(),name='login'),
    path('token/refresh/',TokenRefreshView.as_view(),name="refresh"),
    path("upload-pdf/",DocumentUploadView.as_view(),name="upload-pdf"),
    path('ask/',AskQuestionView.as_view(),name="ask"),
    path('get-users/',GetUsersView.as_view(),name="list-user"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)