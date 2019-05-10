import boto3
from Final import main
from moto import mock_ec2

print_verbos = False

def print_log(s):
    if print_verbos: print(s)

@mock_ec2
def no_tags():

    # Creating running test instances with no tags
    client = boto3.client('ec2', region_name='us-west-1')
    client.run_instances(ImageId="ami-1234abcd", MinCount=4, MaxCount=4)

    # Stopping running instances with no tags
    print("Running with no tags and running instances")
    main(0,0)
    client = boto3.client('ec2', region_name='us-west-1')
    instances = client.describe_instances()['Reservations'][0]['Instances']
    print_log(instances)
    if any_running(instances): raise ValueError('Instance running when it shouldn\'t be')
    print()

    # Stopping stoped instances with no tags
    print("Running again with no tags and stopped instances")
    main(0,0)
    client = boto3.client('ec2', region_name='us-west-1')
    instances = client.describe_instances()['Reservations'][0]['Instances']
    print_log(instances)
    if any_running(instances): raise ValueError('Instance running when it shouldn\'t be')
    print()

@mock_ec2
def irrelevant_tags():

    # Creating running test instances with irrelevant tags
    client = boto3.client('ec2', region_name='us-west-1')
    client.run_instances(ImageId="ami-1234abcd", MinCount=4, MaxCount=4,TagSpecifications=[{"ResourceType":"instance","Tags":[{"Key":"test","Value":"test"}]}])

    # Stopping running instances with irrelevant tags
    print("Running with irrelevant tags and running instances")
    main(0,0)
    client = boto3.client('ec2', region_name='us-west-1')
    instances = client.describe_instances()['Reservations'][0]['Instances']
    print_log(instances)
    if any_running(instances): raise ValueError('Instance running when it shouldn\'t be')
    print()

    # Stopping stoped instances with irrelevant tags
    print("Running again with irrelevant tags and stopped instances")
    main(0,0)
    client = boto3.client('ec2', region_name='us-west-1')
    instances = client.describe_instances()['Reservations'][0]['Instances']
    print_log(instances)
    if any_running(instances): raise ValueError('Instance running when it shouldn\'t be')
    print()

@mock_ec2
def preserve_tags():

    # Creating running test instances with preserve tags
    client = boto3.client('ec2', region_name='us-west-1')
    client.run_instances(ImageId="ami-1234abcd", MinCount=4, MaxCount=4,TagSpecifications=[{"ResourceType":"instance","Tags":[{"Key":"preserve","Value":""}]}])

    # Atempting to stop running instances with preserve tags. Should not stop
    print("Running with preserve tags and running instances")
    main(0,0)
    client = boto3.client('ec2', region_name='us-west-1')
    instances = client.describe_instances()['Reservations'][0]['Instances']
    print_log(instances)
    if not all_running(instances): raise ValueError('Instance stopped when it shouldn\'t be')
    print()


def any_running(instances):
    running = False
    for instance in instances:
        if instance["State"]["Code"] == 16:
            running = True
    return running

def all_running(instances):
    running = True
    for instance in instances:
        if instance["State"]["Code"] != 16:
            running = False
    return running


no_tags()

irrelevant_tags()

preserve_tags()