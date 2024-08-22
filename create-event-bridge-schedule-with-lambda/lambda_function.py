import boto3
from datetime import datetime
import json

# Default configurations
default_iam_role_arn = 'arn:aws:iam::240993297305:role/allow-event-bridge-invoke-lambda-role'
default_add_payload = {"identifier": "hhe-eql-document-clusters", "action": "add", "db_type": "db.r5.xlarge", "quantity": "2"}
default_remove_payload = {"identifier": "hhe-eql-document-clusters", "action": "remove", "db_type": "db.r5.xlarge", "quantity": "2"}
date_format = '%Y-%m-%d %H:%M:%S'

def create_schedule(boto3_client, sub_event):
    try:
        # Description for the schedule
        schedule_description = f"Create event bridge schedule to invoke {sub_event['TargetLambdaFncName']} function at {sub_event['StartTime']}"
        
        # Parse the start time to the required format
        local_datetime = datetime.strptime(sub_event['StartTime'], date_format)
        
        # Adjust payloads based on event data
        payload = default_add_payload if sub_event.get('ScaleOut', False) else default_remove_payload
        payload["db_type"] = sub_event.get('DbType', "db.r5.xlarge")
        payload["quantity"] = str(sub_event.get('NumberOfAdjustment', "2"))
        
        # Creating the schedule
        response = boto3_client.create_schedule(
            Name=sub_event['ScheduledActionName'],
            Description=schedule_description,
            GroupName=sub_event.get('ScheduleGroupName'),
            ActionAfterCompletion='DELETE',
            FlexibleTimeWindow={'Mode': 'OFF'},
            ScheduleExpression=f"at({local_datetime.isoformat()})",
            ScheduleExpressionTimezone=sub_event['TimeZone'],
            State=sub_event.get('State', 'ENABLED'),
            Target={
                'Arn': sub_event['TargetLambdaFncArn'],
                'Input': json.dumps(payload),  # Pass the payload as input
                'RoleArn': default_iam_role_arn,
                'RetryPolicy': {
                    'MaximumEventAgeInSeconds': 86400, # 24 hours
                    'MaximumRetryAttempts': 185
                }
            }
        )
        
        return {
            'success': True,
            'event_name': sub_event['ScheduledActionName']
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'event_name': sub_event['ScheduledActionName']
        }

def check_schedule_group_exist(schedule_groups, group_name):
    return any(d['Name'] == group_name for d in schedule_groups)

def lambda_handler(event, context):
    client = boto3.client('scheduler')
    
    success_events = []
    failure_events = []

    # Get existing schedule groups
    schedule_groups = client.list_schedule_groups()
    print('schedule_groups :', schedule_groups.get('ScheduleGroups', []))
    
    for sub_event in event['ScheduledUpdateGroupActions']:
        group_name = sub_event.get('ScheduleGroupName', 'default')
        # Set common parameters for each sub-event
        sub_event['TimeZone'] = event['TimeZone']
        sub_event['TargetLambdaFncName'] = event['TargetLambdaFncName']
        sub_event['TargetLambdaFncArn'] = event['TargetLambdaFncArn']
        sub_event['ScheduleGroupName'] = group_name if check_schedule_group_exist(schedule_groups.get('ScheduleGroups', []), group_name) else 'default'
        
        # create schedule
        result = create_schedule(client, sub_event)
        
        if result['success']:
            success_events.append(result['event_name'])
        else:
            failure_events.append({
                'event_name': result['event_name'],
                'error': result['error']
            })

    return {
        'statusCode': 200 if not failure_events else 500,
        'success_events': success_events,
        'failure_events': failure_events
    }
