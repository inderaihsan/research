from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [
    path("hello/", views.init), 
    path("upload-geojson", views.upload_data_to_postgis), 
    path("get-posyandu-data", views.get_posyandu_data), 
    path("get-posyandu-data-query", views.get_posyandu_query), 
    path("get-wadmkc", views.get_wadmkc), 
    path("get-wadmkd", views.get_wadmkd), 
]
