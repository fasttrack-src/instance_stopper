# Notes

## Cloudformation File

### Example AWS Lambda Cloudformation file.

```json
{
  "Type" : "AWS::Lambda::Function",
  "Properties" : {
    "Code" : Code, // Further Down in notes.md
    "DeadLetterConfig" : DeadLetterConfig, // N/A
    "Description" : String, // Just a description
    "Environment" : Environment, // N/A
    "FunctionName" : String, // Just a name
    "Handler" : String, // index.(the name of the handler function)
    "KmsKeyArn" : String, // N/A
    "Layers" : [ String, ... ], // N/A
    "MemorySize" : Integer, // May be Useful
    "ReservedConcurrentExecutions" : Integer, // N/A
    "Role" : String, // The IAM Role of the Lambda Code
    "Runtime" : String, // python3.7 or python3.6
    "Timeout" : Integer, // May be useful
    "TracingConfig" : TracingConfig, // N/A
    "VpcConfig" : VPCConfig, // N/A
    "Tags" : [ Resource Tag, ... ] // N/A
  }
}
```

### Rough Format of of Code

```json
"ZipFile" : { "Fn::Join" : ["\n", [
  "import json",
  "import cfnresponse",
  "def handler(event, context):",
  "   responseValue = int(event['ResourceProperties']['Input']) * 5",
  "   responseData = {}",
  "   responseData['Data'] = responseValue",
  "   cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, \"CustomResourcePhysicalID\")"
]]}
```

### Real Example code
```json
"ZipFile" : { "Fn::Join" : ["\n", ["import boto3,pprint", "", "regions = [\"us-east-2\",\"us-east-1\",\"us-west-1\",\"us-west-2\",\"ap-south-1\",\"ap-northeast-3\",\"ap
-northeast-2\",\"ap-southeast-1\",\"ap-southeast-2\",\"ap-northeast-1\",\"ca-central-1\",\"cn-north-1\",\"cn-northwest-1\",\"eu-central-1\",\"eu-west-1\",\"eu-west-2\",
\"eu-west-3\",\"eu-north-1\",\"sa-east-1\"]", "", "def printregion(ec2):", "try:", "response = ec2.describe_instances()", "# iid = []", "# if \"Instances\" in response[
\"Reservations\"]:", "#     for i in response[\"Reservations\"][\"Instances\"]:", "#         iid += i[\"InstanceId\"]", "#     print(iid)", "if len(response[\"Reservati
ons\"]) > 0:", "for reservation in response[\"Reservations\"]:", "if len(reservation[\"Instances\"]) > 0:", "for instance in reservation[\"Instances\"]:", "print(instan
ce[\"InstanceId\"])", "print(instance[\"State\"][\"Code\"])", "print(instance[\"Tags\"])", "if checktags(instance[\"Tags\"],\"kill_daily\"):", "print(\"This shouldn't b
e killed\")", "# pprint.pprint(instance)", "except:", "pass", "", "def getidforkillingregion(ec2,searchkey):", "try:", "response = ec2.describe_instances()", "iid = []"
, "rnkiid = []", "for reservation in response[\"Reservations\"]:", "for instance in reservation[\"Instances\"]:", "if instance[\"State\"][\"Code\"] == 16 and checktags(
instance[\"Tags\"],searchkey) == False:", "iid.append(instance[\"InstanceId\"])", "if instance[\"State\"][\"Code\"] == 16 and checktags(instance[\"Tags\"],searchkey):",
 "rnkiid.append(instance[\"InstanceId\"])", "# print(instance[\"InstanceId\"],\" is running but does not want to be killed.\")", "return iid,rnkiid", "except:", "return
 [],[]", "", "def checktags(tags,searchkey):", "for tag in tags:", "if tag[\"Key\"] == searchkey:", "return True", "return False", "", "", "#Main Program", "", "for reg
ion in regions:", "ec2 = boto3.client('ec2',region_name=region)", "iid,rnkiid = getidforkillingregion(ec2,\"kill_daily\")", "if len(iid) > 0 or len(rnkiid) > 0:", "prin
t(region)", "# printregion(ec2)", "print(\"These Instance's want to be stopped \",iid)", "print(\"These Instance's are running but don't want to be stopped \",rnkiid)"]
]}
```


### Possibly Correct Policy 

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1553766506710",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StopInstances"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:ec2:*:*:*/*"
    }
  ]
}
```

### Full AWS IAM Role Cloudformation
```json
{
  "Type": "AWS::IAM::Role",
  "Properties": {
    "AssumeRolePolicyDocument": {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "Stmt1553766506710",
            "Action": [
              "ec2:DescribeInstances",
              "ec2:StopInstances"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:ec2:*:*:*/*"
        }]
      },
    "Path": "/", // Nessisary
    "Policies": [ {
      "PolicyName": "EC2 Killer Policy",
      "PolicyDocument": {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "Stmt1553766506710",
            "Action": [
              "ec2:DescribeInstances",
              "ec2:StopInstances"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:ec2:*:*:*/*"
        }]
      }
    }],
    "RoleName": "EC2 Killer Role"
  }
}
```

### Cloud Watch

```json
{
  "Type" : "AWS::Events::Rule",
  "Properties" : {
    "Description" : "This rule is used to trigger EC2 Killer Every Day at 11pm to kill instances which are not protected",
    "Name" : "EC2 Killer Event",
    "ScheduleExpression" : "cron(0 11 * * ? *)",
    "State" : "ENABLED",
    "Targets" : [{
      "Arn": { "Fn::GetAtt": ["LambdaFunction", "Arn"] },
      "Id": "TargetFunctionV1"
    }]
  }
}
```

### Useful ARN
Basic Execution Policy ARN `arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole`

## Useful Links

### Lambda 

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-code
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-deadletterconfig.html
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html

### Cloud Watch Events

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html

### IAM Roles and Polices

https://awspolicygen.s3.amazonaws.com/policygen.html
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-templateexamples
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html