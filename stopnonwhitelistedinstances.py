import boto3, json
from botocore.exceptions import ClientError

run = False

# Importing whitelist.json to an array called whitelist
with open("whitelist.json") as f:
    whitelist = json.load(f)

print(whitelist)

# Connecting to aws with the credentials associated with your acount
ec2 = boto3.client('ec2')

# Getting a description of the instances from aws
response = ec2.describe_instances()

# Printing this description for testing
# print(response)

# Getting all the instance ids and storing them in an array
iid = []
if "Instances" in response["Reservations"]:
    for i in response["Reservations"]["Instances"]:
        # This ensures only running instances are stopped
        if i["State"]["Code"] == 16:
            iid += i["InstanceId"]
        print(i["Tags"])
    print(iid)

# Getting all the non whitlisted instance ids and storing them in an array
instance_ids = [el for el in iid if el not in whitelist]
print(instance_ids)

# This section does the actual stopping of the instances
# This also checks to ensure that there is an instance to be stopped.
if len(instance_ids) > 0:
    # This is a dry run test to ensure you have the correct perms to stop the instances
    try:
        ec2.stop_instances(InstanceIds=instance_ids, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # This checks that it isn't a dev build
    if run:
        # This ask the user wheather they want to stop instances. This can be removed for final version
        cont = input("Would you like to stop instances. Y to continue")
        if cont == "Y":

            # Dry run succeeded, call stop_instances without dryrun
            # This stops instances
            try:
                response = ec2.stop_instances(InstanceIds=instance_ids, DryRun=False)
                print(response)
            except ClientError as e:
                print(e)