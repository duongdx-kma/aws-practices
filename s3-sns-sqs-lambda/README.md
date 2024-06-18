# Stack: S3 -> SNS TOPIC Filter -> SQS -> Lambda:

- ### step1: create s3 bucket: duongdx-testing

- ### step2: Go to SNS console -> create SNS topic: sns-fan-out
```
- check and edit SNS access policy
```

- ### step3: Go to SQS console -> create SQS: sqs-image
```
- check and edit SQS access policy
```

- ### step4: Go to SQS console -> create SQS: sqs-video
```
- check and edit SQS access policy
```

- ### step5: Go to SQS console -> create SQS: sqs-dead-letter-queue
```
- check and edit SQS access policy
```

- ### step6: Go to Lambda console -> create Lambda function: Lambda-image, Lambda-video
```
- check and edit Lambda role
```

- ### step7: Go to s3 console -> create Event Notification for s3 bucket:
```
- Push message to SNS topic
```


- ### step8: Go to SNS console -> create SNS Topic Subscriber:
```
- create SNS Topic Subscriber -> SQS image

- create SNS Topic Subscriber -> SQS video
```

- ### step9: Go to SQS console -> create Lambda trigger:
- create Lambda trigger -> Lambda image

- create Lambda trigger -> Lambda video
```