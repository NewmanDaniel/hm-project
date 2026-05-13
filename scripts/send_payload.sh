#!/bin/bash
# Usage: ./send_payload.sh <TOKEN> <DEVICE_EUI> <FCNT> <STATUS(pass/fail)>

TOKEN=$1
DEVICE=$2
FCNT=$3
STATUS=$4

if [ "$STATUS" == "pass" ]; then
    DATA="AQ==" # 01
else
    DATA="AA==" # 00
fi

echo "Sending Payload: Device=$DEVICE, fCnt=$FCNT, Status=$STATUS"

curl -X POST http://127.0.0.1:8000/api/payloads/ \
     -H "Authorization: Token $TOKEN" \
     -H "Content-Type: application/json" \
     -d "{
           \"fCnt\": $FCNT,
           \"devEUI\": \"$DEVICE\",
           \"data\": \"$DATA\"
         }"
echo -e "\n"
