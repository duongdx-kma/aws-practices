from datetime import datetime, timezone, timedelta
import boto3
import json

date_format = '%Y-%m-%d %H:%M:%S'

time_zone_offsets = {
    "Asia/Seoul": 9,    # UTC+9
}

def convert_raw_data(schedule_data, time_zone):
    offset_hours = time_zone_offsets.get(time_zone, 0)  # Default to UTC if time_zone is not found
    local_tz = timezone(timedelta(hours=offset_hours))
    print('offset_hours', offset_hours)
    print('local_tz', local_tz)
    for data in schedule_data:
        data['TimeZone'] = time_zone
        local_datetime = datetime.strptime(data['StartTime'], date_format)

        # Localize the datetime (make it timezone-aware)
        localized_datetime = local_datetime.replace(tzinfo=local_tz)

        # Convert to UTC
        utc_datetime = localized_datetime.astimezone(timezone.utc)
        
        # Print as string
        utc_datetime_str = utc_datetime.strftime(date_format)
        data['StartTime'] = utc_datetime_str

    return schedule_data


def lambda_handler(event, context):
    client = boto3.client('autoscaling')
    
    # Retrieve parameters from the event
    auto_scaling_group_name = event.get('AutoScalingGroupName', '')
    scheduled_raw_data = event.get('ScheduledUpdateGroupActions', [])
    time_zone = event.get('TimeZone')

    scheduled_actions = convert_raw_data(scheduled_raw_data, time_zone)

    try:
        # Create the batch of scheduled actions
        response = client.batch_put_scheduled_update_group_action(
            AutoScalingGroupName=auto_scaling_group_name,
            ScheduledUpdateGroupActions=scheduled_actions
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Scheduled actions created successfully.'),
            'details': response
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

