import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client("ec2")

instance_ids = []

try:
    ec2.stop_instances(InstanceIds=instance_ids, DryRun=True)
except ClientError as e:
    if 'DryRunOperation' not in str(e):
        raise

# Dry run succeeded, call stop_instances without dryrun
try:
    response = ec2.stop_instances(InstanceIds=instance_ids, DryRun=False)
    print(response)
except ClientError as e:
    print(e)