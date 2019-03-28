import boto3,pprint

regions = ["us-east-2","us-east-1","us-west-1","us-west-2","ap-south-1","ap-northeast-3","ap-northeast-2","ap-southeast-1","ap-southeast-2","ap-northeast-1","ca-central-1","cn-north-1","cn-northwest-1","eu-central-1","eu-west-1","eu-west-2","eu-west-3","eu-north-1","sa-east-1"]

def printregion(ec2):
    try:
        response = ec2.describe_instances()
        # iid = []
        # if "Instances" in response["Reservations"]:
        #     for i in response["Reservations"]["Instances"]:
        #         iid += i["InstanceId"]
        #     print(iid)
        if len(response["Reservations"]) > 0:
            for reservation in response["Reservations"]:
                if len(reservation["Instances"]) > 0:
                    for instance in reservation["Instances"]:
                        pprint.pprint(instance)
    except:
        pass

for region in regions:
    ec2 = boto3.client('ec2',region_name=region)
    print(region)
    printregion(ec2)