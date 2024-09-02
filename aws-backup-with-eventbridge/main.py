import urllib3
import json
import os

from datetime import datetime, timedelta

http = urllib3.PoolManager()

teams_hook_url = os.environ['hook_url']

def lambda_handler(event, context):
    print(event)

    # Extract message content from the event
    detailMessage = event["detail"]

    # convert timestamps
    rawTime = event.get("time", "N/A")
    utcTime = datetime.strptime(rawTime,  "%Y-%m-%dT%H:%M:%SZ")
    localTime = utcTime + timedelta(hours=9)

    # Extract specific items from message att content
    msgAlarmName = event.get("detail-type", "N/A")
    msgAccount = event.get("account", "N/A")
    backupId = detailMessage.get("backupJobId", "N/A")
    backupVaultName = detailMessage.get("backupVaultName", "N/A")
    msgTime = localTime.strftime("%Y-%m-%d %H:%M:%S")
    msgEventTypeCode = detailMessage.get("state", "N/A")
    msgDescription = detailMessage.get("statusMessage", "N/A")

    # Create Adaptive Card content
    body = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "msteams": {
                    	"width": "Full"
                    },
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": f"⚠️ {msgAlarmName}",
                            "weight": "bolder",
                            "size": "Large"
                        },
                        {
                            "type": "TextBlock",
                            "text": f"ㆍ 계정 : {msgAccount}",
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": f"ㆍ Backup Vault: {backupVaultName}",
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": f"ㆍ 백업 ID : {backupId}",
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": f"ㆍ 이벤트 발생 시간 : {msgTime}",
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": f"ㆍ 분류 : {msgEventTypeCode}",
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": f"ㆍ 메시지 : {msgDescription}",
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }
    
    # Encode the contents of the message in UTF-8 and convert it to json format
    bodyjson = json.dumps(body).encode('utf-8')

    # Send to Teams
    resp = http.request('POST', teams_hook_url, body=bodyjson, headers={'Content-Type': 'application/json'})
    
    # Log the response status and data
    print(f"Response status: {resp.status}")
    print(f"Response data: {resp.data.decode('utf-8')}")

    return {
        'statusCode': resp.status,
        'body': resp.data.decode('utf-8')
    }
