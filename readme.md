# EC2 Instance Stopper

This just stops all EC2 instances which do not have a key the key `preserve` set.
The cloudformation
The final cloud formation file is generated by a python program, this is beacuse the cloudformation file has the AWS lambda code embeded within it.

## Setup to use from cloudformation file
1.  Get the file from the release page (or from source below)
2.  Open and login to AWS.
3.  Go to the dashboard and select cloudformation
4.  Click Create Stack
5.  Then use upload a template to s3 to upload the template, click next
6.  Name your stack and continue
7.  Click through and accept then create.
8.  Your done, now wait till 11pm for the little elves to shut down your instances.

## Setup to use (from source)

1.  Use pytest to run `complete_test.py` to ensure that the code works as intended
    1.  if it produces an error submit an issue
    2.  Currently there are 2 warnings don't worry about these
2.  Run `CFGenerator.py` to get a new cloudformation file.
    1.  Currently it is set to run the ec2 instance stopper at 11 o'clock local time. This can be changed in the `config.json` file
    2.  `template.json` is responsible for the pattern of the cloudformation file.
3.  After you have run the `CFGenerator.py` you will have a file called `cloudformgened.json`. This can be used with cloudformation to launch ec2 stopper
4.  On your aws console open the cloudformation section and use the file `cloudformgened.json` to lanuch ec2 instance stopper. Read Setup to use from cloudformation file if you don't know how to do this.


## What each file is

File|Use
-|-
`EC2_Instance_Stopper.py`|This is the code of the instance stopper it's self
`CFGenerator.py`|This is used to generate a cloudformation file
`README.md`|Clue is in the name (this file)
`config.json`|This is the configeration file for the CFGenerator
`regions.txt`|This is a copy of the aws region names
`template.json`|This is the template for the cloudformation file
`complete_test.py`|This is used to test the instance stopper is working correctly