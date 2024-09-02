# Monitor AWS Backup using EventBridge

## I. Create AWS Backup

### step-01. create `Backup Vault` to manage `snapshot`: name `critical-vault`

### step-02. create `IAM Role`  for create `BackupVault`

### step-03. create `Backup plan`

#### step-03-01. create `Backup rule`
```t
# backup retention period: 1 day

# backup vault: name `critical-vault`
```

#### step-03-02. create `Resource assignments`
```t
# choose the aws resource
```

## II. Create `AWS EventBridge Rule`

### step-01: Create `EventBridge Rule`
```t
# name: aw-backup-fail-rule

# Event Bus: default

# event pattern:
{
  "source": ["aws.backup"],
  "detail-type": ["Backup Job State Change"],
  "detail": {
    "state": ["FAILED", "ABORTED"]
  }
}

# destination: Choose Lambda Function
```

