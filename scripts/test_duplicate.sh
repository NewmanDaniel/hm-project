#!/bin/bash
# Usage: ./test_duplicate.sh <TOKEN> <DEVICE_EUI>

TOKEN=$1
DEVICE=$2

echo "Test 1: Sending initial payload (fCnt=1)..."
curl -s -X POST http://127.0.0.1:8000/api/payloads/ \
     -H "Authorization: Token $TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"fCnt\": 1, \"devEUI\": \"$DEVICE\", \"data\": \"AQ==\"}" > /dev/null

echo "Test 2: Sending DUPLICATE payload (fCnt=1)..."
curl -X POST http://127.0.0.1:8000/api/payloads/ \
     -H "Authorization: Token $TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"fCnt\": 1, \"devEUI\": \"$DEVICE\", \"data\": \"AQ==\"}"

echo -e "\nExpected: A 400 Bad Request with 'Duplicate' error."
