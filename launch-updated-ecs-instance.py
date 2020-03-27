import boto3
import sys, getopt
import json

# Print Usage instructions
def usage():
    print("Usage:")
    print("python3 launch-updated-ecs-instance.py [options]")
    print()
    print("Options:")
    print("--help\t\t\tPrint usage instructions")
    print("--region\t\tThe region")
    print("--instance-type\t\tThe instance type for the ECS instance")
    print("--key\t\t\tThe SSH key pair")
    print("--count\t\t\tThe number of instances to launch")
    print("--security-group\tThe \"ID\" of the security group to attach to the ECS instance")
    print("--subnet\t\tThe \"ID\" of the subnet for the ECS instance to be launched in")
    print("--iam-role\t\tThe \"Name\" of the IAM Role which must be attached to the instance")
    print("--cluster\t\tThe Cluster Name")
    print("--user-data\t\tThe path to a custom User Data script")
    print("\nNote: If you specify both a cluster and a user data location, the user data will take preference")


def main(argv):

#initialize argument parameters dictionary
    params = {
          "region=": '',
          "instance-type=": '',
          "key=": '',
          "count=": '1',
          "security-group=": '',
          "subnet=": '',
          "iam-role=": '',
          "cluster=": '',
          "user-data=": ''
    }

# Add help option to arguments
    arguments = list(params.keys())
    arguments.append("help")

    try:
      opts, args = getopt.getopt(argv,'',arguments)

    except getopt.GetoptError:
      usage()
      sys.exit(2)
      
    for opt, arg in opts:

      if opt in ('--help'):
        usage()
        sys.exit()

      else:
        for key, val in params.items():
          if opt in ("--" + key):
            params[key] = arg

  # If User Data file specified, read data from file
    if(len(params["user-data="]) > 0):
      user_data = open(params["user-data="], "r+")
      user_data_text = user_data.read()
      params["user-data="] = user_data_text

  # If User Data file is not present, create user data with cluster ID
    if(len(params["user-data="]) == 0) and (len(params["cluster="]) > 0):
      user_data ='''#!/bin/bash
mkdir -p /etc/ecs
touch /etc/ecs/ecs.config
echo "ECS_CLUSTER={0}" >> /etc/ecs/ecs.config
'''
      user_data_text = user_data.format(params["cluster="])
      params["user-data="] = user_data_text
    
    ec2client = ''
    ssmclient = ''

  # If region specified, create client with region defined, else region obtained from credentials or environment variable
    if(len(params['region=']) > 0):
      ec2client = boto3.client('ec2', params["region="])
      ssmclient = boto3.client('ssm', params["region="])
    
    else:
      ec2client = boto3.client('ec2')
      ssmclient = boto3.client('ssm')

    response = ssmclient.get_parameter(
    Name = '/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id')

    ami_id = response['Parameter']['Value']

    response = ec2client.run_instances(
    ImageId = ami_id,
    InstanceType = params["instance-type="],
    KeyName = params["key="],
    SecurityGroupIds = [
      params["security-group="]
    ],
    MaxCount = int(params["count="]),
    MinCount = int(params["count="]),
    SubnetId = params["subnet="],
    IamInstanceProfile={
        'Name': params["iam-role="]
    },
    UserData = params["user-data="])

    print("Instances launched successfully")

    print("\nNumber of Instances:\t" , len(response["Instances"]))
    print("\nInstance Details:")

    for instance in response["Instances"]:
      print("\nInstance ID:\t" , instance['InstanceId'])
      print("Private IP:\t" , instance['PrivateIpAddress'])
    
    print("\nFull response output")
    print(response)
    
    #print(response)


if __name__ == "__main__":
   main(sys.argv[1:])