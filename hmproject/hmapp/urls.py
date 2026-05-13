#!/usr/bin/env python3

from django.urls import path
from . import views

urlpatterns = [
    path('api/payloads/', views.PayloadIngestView.as_view(), name='payload-ingest'),
    path('api/devices/', views.DeviceStatusListView.as_view(), name='device-status'),
]
