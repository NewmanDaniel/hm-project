#!/usr/bin/env python3

import base64
from rest_framework import serializers
from .models import Device, Payload

class PayloadIngestSerializer(serializers.Serializer):
    fCnt = serializers.IntegerField()
    devEUI = serializers.CharField(max_length=16)
    data = serializers.CharField()

    def validate_data(self, value):
        try:
            # Decode base64 to bytes, then convert to hex string
            decoded_bytes = base64.b64decode(value)
            hex_value = decoded_bytes.hex()

            # Convert value to integer
            value_as_int = int.from_bytes(decoded_bytes, byteorder='big')

            # Check if value is 1 (represented as '01' in hex for a single byte)
            is_passing = (value_as_int == 1)

            # Attach to serializer for later use
            self.context['data_hex'] = hex_value
            self.context['is_passing'] = is_passing

            return value
        except Exception as e:
            raise serializers.ValidationError(f"Invalid Base64 data: {e}")

    def validate(self, data):
        devEUI = data.get('devEUI')
        fCnt = data.get('fCnt')

        # Check for duplicate fCnt for this device
        if Device.objects.filter(devEUI=devEUI).exists():
            device = Device.objects.get(devEUI=devEUI)
            if Payload.objects.filter(device=device, fCnt=fCnt).exists():
                raise serializers.ValidationError("Duplicate fCnt for this device.")

        return data

class DeviceStatusSerializer(serializers.ModelSerializer):
    latest_status = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ['devEUI', 'name', 'latest_status']

    def get_latest_status(self, obj):
        latest_payload = obj.payloads.order_by('-fCnt').first()
        if latest_payload:
            return "Passing" if latest_payload.is_passing else "Failing"
        return "No Data"
