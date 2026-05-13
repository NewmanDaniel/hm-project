from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Device, Payload
from .serializers import PayloadIngestSerializer, DeviceStatusSerializer

class PayloadIngestView(APIView):
    """
    Receives payload from IoT devices.
    """
    def post(self, request):
        serializer = PayloadIngestSerializer(data=request.data)
        if serializer.is_valid():
            devEUI = serializer.validated_data['devEUI']

            # Get or Create Device
            device, created = Device.objects.get_or_create(
                devEUI=devEUI,
                defaults={'name': f'Device {devEUI}'}
            )

            # Create Payload
            Payload.objects.create(
                device=device,
                fCnt=serializer.validated_data['fCnt'],
                data_raw=serializer.validated_data['data'],
                data_hex=serializer.context.get('data_hex', ''),
                is_passing=serializer.context.get('is_passing', False)
            )

            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceStatusListView(APIView):
    """
    Lists all devices and their current status.
    """
    def get(self, request):
        devices = Device.objects.all()
        serializer = DeviceStatusSerializer(devices, many=True)
        return Response(serializer.data)
