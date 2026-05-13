from django.db import models

from django.db import models

class Device(models.Model):
    devEUI = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=100, blank=True, default='Unknown Device')

    def __str__(self):
        return self.devEUI

class Payload(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='payloads')
    fCnt = models.IntegerField()
    data_raw = models.CharField(max_length=255) # Store original base64
    data_hex = models.CharField(max_length=255, blank=True)
    is_passing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['device', 'fCnt'], name='unique_fcnt_per_device')
        ]

    def __str__(self):
        return f"Payload {self.fCnt} from {self.device.devEUI}"
