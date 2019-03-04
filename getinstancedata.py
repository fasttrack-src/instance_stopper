import boto3

ec2 = boto3.client('ec2')
response = ec2.describe_instances()
iid = []
if "Instances" in response["Reservations"]:
    for i in response["Reservations"]["Instances"]:
        iid += i["InstanceId"]
    print(iid)
print(response)