from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ai/<int:id>', views.validate, name="validate"),
    path('upload', views.upload, name="upload"),
    path('upload/<int:id>', views.upload_with_image, name="upload_with_image"),
]