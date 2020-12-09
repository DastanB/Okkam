from django.contrib import admin
from django.urls import path

from rest_framework import routers

from .views import WebPageViewSet

router = routers.DefaultRouter()
router.register('site_check', WebPageViewSet, basename='main')

urlpatterns = [] + router.urls