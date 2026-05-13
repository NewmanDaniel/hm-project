#!/bin/bash
# Usage: ./get_devices.sh <TOKEN>

TOKEN=$1

echo "Fetching Device Statuses..."
curl -X GET http://127.0.0.1:8000/api/devices/ \
     -H "Authorization: Token $TOKEN"
echo -e "\n"
