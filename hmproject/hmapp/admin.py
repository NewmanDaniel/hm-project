from django.contrib import admin
from .models import Device, Payload

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('devEUI', 'name')

@admin.register(Payload)
class PayloadAdmin(admin.ModelAdmin):
    list_display = ('device', 'fCnt', 'is_passing', 'created_at')
