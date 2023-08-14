from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('edit/<str:pk>', views.editVideo, name='edit'),
    path('upload', views.uploadVideo, name='upload'),
    path('delete/<str:pk>', views.deleteVideo, name='delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)