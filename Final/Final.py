import boto3,pprint

run = False

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
                        print(instance["InstanceId"])
                        print(instance["State"]["Code"])
                        print(instance["Tags"])
                        if checktags(instance["Tags"],"kill_daily"):
                            print("This shouldn't be killed")
                        # pprint.pprint(instance)
    except:
        pass

def getidforkillingregion(ec2,searchkey):
    try:
        response = ec2.describe_instances()
        iid = []
        rnkiid = []
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if instance["State"]["Code"] == 16 and checktags(instance["Tags"],searchkey) == False:
                    iid.append(instance["InstanceId"])
                if instance["State"]["Code"] == 16 and checktags(instance["Tags"],searchkey):
                    rnkiid.append(instance["InstanceId"])
                    # print(instance["InstanceId"]," is running but does not want to be killed.")
        return iid,rnkiid
    except:
        return [],[]

def checktags(tags,searchkey):
    for tag in tags:
        if tag["Key"] == searchkey:
            return True
    return False

def stopinstances(ec2,iid):
    # This section does the actual stopping of the instances
    # This also checks to ensure that there is an instance to be stopped.
    instance_ids = iid
    if len(instance_ids) > 0:
        # This is a dry run test to ensure you have the correct perms to stop the instances
        try:
            ec2.stop_instances(InstanceIds=instance_ids, DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # This checks that it isn't a dev build
        if run:
            # Dry run succeeded, call stop_instances without dryrun
            # This stops instances
            try:
                response = ec2.stop_instances(InstanceIds=instance_ids, DryRun=False)
                print(response)
            except ClientError as e:
                print(e)

#Main Program
def main(e,c):
    for region in regions:
        ec2 = boto3.client('ec2',region_name=region)
        iid,rnkiid = getidforkillingregion(ec2,"kill_daily")
        stopinstances(ec2,iid)
        if len(iid) > 0 or len(rnkiid) > 0:
            print(region)
            # printregion(ec2)
            print("These Instance's want to be stopped ",iid)
            print("These Instance's are running but don't want to be stopped ",rnkiid)
