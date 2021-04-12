from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
	path('', views.index, name="sunsris"),
	# path('scraper/', views.scraper, name="scrapersunsris"),
	path('result/', views.result, name="resultsunsris"),

]
