# Notification options with AWS Backup

## I. Notification options with AWS Backup
```
AWS Backup jobs fail  → SNS Topic → Lambda → Teams
```
### Step 1: Create Lambda function: Lambda is Subscriptions of SNS topic  

### Step 2: Create SNS topic and access policy
```json
{
  "Version": "2008-10-17",
  "Id": "__default_policy_ID",
  "Statement": [
    {
      "Sid": "__default_statement_ID",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": [
        "SNS:Publish",
        "SNS:RemovePermission",
        "SNS:SetTopicAttributes",
        "SNS:DeleteTopic",
        "SNS:ListSubscriptionsByTopic",
        "SNS:GetTopicAttributes",
        "SNS:AddPermission",
        "SNS:Subscribe"
      ],
      "Resource": "arn:aws:sns:<region>:<account-id>:<sns-topic-name>",
      "Condition": {
        "StringEquals": {
          "AWS:SourceOwner": "account-id"
        }
      }
    },
    {
      "Sid": "My-statement-id",
      "Effect": "Allow",
      "Principal": {
        "Service": "backup.amazonaws.com"
      },
      "Action": "SNS:Publish",
      "Resource": "arn:aws:sns:<region>:<account-id>:<sns-topic-name>"
    }
  ]
}
```

### Step 3: configure SNS topic Subscriptions invoke to Lambda function (which created in step 1)

### Step 4: Configure your backup vault to send notifications to the SNS topic
```powershell
# Command line:
aws backup put-backup-vault-notifications \
    --backup-vault-name <backup-vault-name> \
    --sns-topic-arn arn:aws:sns:<region>:<account-id>:<sns-topic-name> \
    --backup-vault-events "BACKUP_JOB_FAILED"
```

### step 5: confirm that notifications are configured
```powershell
# command:
aws backup get-backup-vault-notifications --backup-vault-name <backup-vault-name>

# result:
{
    "BackupVaultName": "testiing-vault",
    "BackupVaultArn": "arn:aws:backup:<region>:<account-id>:backup-vault:<backup-vault-name>",
    "SNSTopicArn": "arn:aws:sns:<region>:<account-id>:<sns-topic-name>",
    "BackupVaultEvents": [
        "BACKUP_JOB_FAILED"
    ]
}
```

### Step 6: check lambda log:
```
the function event is: {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:ap-southeast-1:xxxxxxx:backup-fail:6a89fc17-7114-4c7c-9f61-9fa605278e6d', 'Sns': {'Type': 'Notification', 'MessageId': '9b01f85b-f3f5-5bab-a134-a71c56e45fb1', 'TopicArn': 'arn:aws:sns:ap-southeast-1:xxxxxxx:backup-fail', 'Subject': 'Notification from AWS Backup', 'Message': 'An AWS Backup job was completed successfully. Recovery point ARN: arn:aws:ec2:ap-southeast-1::image/ami-123456. Backed up Resource ARN : arn:aws:ec2:ap-southeast-1:xxxxxxx:instance/i-123456. Backup Job Id : E16FD778-147E-BBD0-14E9-BC67450BE135', 'Timestamp': '2024-08-27T09:56:33.903Z', 'SignatureVersion': '1', 'Signature': 'oW3Z5Kw2GAFWunOOyGCNnXxGZaIz+zkSKa1lfyDcnGKcoCvUi163nJWhpEBtHgh04Xg663wwtu3zmsbepfkKoiVz2701/18PC0GAaTbaVImt44+udhT5HWlAo/Bgrt7U+BBLP3yUeZbmqQ9VAvsOf5O0unDTQZuIfswo9deHPKKB3MglAOyj8z8UEWskWHqQDotJZslQImUcR8yQqyGf0PPesVc+7yiGM4IYDvzgr0leMzKWL+i5hDlk45oZRBGE154818Mgc4V9hlRWWPLM/cPan2lQAjRvxl5nhqwo0OhLZs9FOfqipiVHod/YO7uPEhxoxTLi2BBF1hx/d+y4uw==', 'SigningCertUrl': 'https://sns.ap-southeast-1.amazonaws.com/SimpleNotificationService-2345678dfghjk.pem', 'UnsubscribeUrl': 'https://sns.ap-southeast-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:ap-southeast-1:xxxxxxx:backup-fail:123456', 'MessageAttributes': {'AccountId': {'Type': 'String', 'Value': 'xxxxxxx'}, 'EventType': {'Type': 'String', 'Value': 'BACKUP_JOB'}, 'State': {'Type': 'String', 'Value': 'COMPLETED'}, 'StartTime': {'Type': 'String', 'Value': '2024-08-27T09:20:00Z'}, 'Id': {'Type': 'String', 'Value': '2345678fghjkl'}}}}]}
```

### Backup Notification with SNS, S3 reference links:
1. https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-notifications.html
2. https://awscli.amazonaws.com/v2/documentation/api/latest/reference/backup/put-backup-vault-notifications.html
3. https://repost.aws/knowledge-center/aws-backup-failed-job-notification
4. https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-notifications.html

## II. Monitoring AWS Backup events using Amazon EventBridge
```
AWS Backup jobs fail  → Event Bridge Rule → SNS Topic → Lambda → Teams
```

### Backup event with EventBridge reference links:
1. https://docs.aws.amazon.com/aws-backup/latest/devguide/eventbridge.html
2. https://repost.aws/knowledge-center/backup-eventbridge-notifications