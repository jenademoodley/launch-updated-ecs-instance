# launch-updated-ecs-instance
A simple python script which launches an Amazon Linux 2 ECS instance from the most updated AMI. The AMI is obtained from AWS Systems Manager:
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami

Pre-requisites:
  - python3
  - boto3
  - IAM User/Role credentials (can be defined as environment variables, through the AWS CLI, or via the IAM Role credentials)
  
 
 Usage of this script is fairly simple. You only need to add the required parameters as arguments.
 
 ```
 $ python3 launch-updated-ecs-instance.py --help
 
Usage:

python3 launch-updated-ecs-instance.py [options]

Options:
--help			Print usage instructions
--region		The region
--instance-type		The instance type for the ECS instance
--key			The SSH key pair
--count			The number of instances to launch
--security-group	The "ID" of the security group to attach to the ECS instance
--subnet		The "ID" of the subnet for the ECS instance to be launched in
--iam-role		The "Name" of the IAM Role which must be attached to the instance
--cluster		The Cluster Name
--user-data		The path to a custom User Data script


Note: If you specify both a cluster and a user data location, the user data will take preference
```

An example usage:
```
python3 launch-updated-ecs-instance.py --key <SSH-KEY> --instance-type <INSTANCE-TYPE> --security-group <SECURITY-GROUP-ID> --subnet <SUBNET-ID> --count <NUMBER-OF-INSTANCES> --cluster <CLUSTER-TO-JOIN>
```
