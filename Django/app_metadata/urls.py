from django.urls import path
from . import views

app_name = "app_metadata"

urlpatterns = [
    path('<int:id>', views.get_meta_data, name='get_metadata'),
    path('data', views.get_data, name='get_data'),
]