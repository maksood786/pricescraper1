from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
	path('', views.index, name="gnews"),
	path('scraper/', views.scraper, name="scraper"),
	path('result/', views.result, name="result"),

]
