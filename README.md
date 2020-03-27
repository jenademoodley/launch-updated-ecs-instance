# launch-updated-ecs-instance
A simple python script which launches an ECS instance from the most updated AMI from AWS Systems Manager.

Pre-requisites:
  - python3
  - boto3
  - IAM User/Role credentials
  
 
 Usage of this script is fairly simple:
 
 $ python3 launch-updated-ecs-instance.py --help
 
Usage:
python3 launch-updated-ecs-instance.py [options]

Options:
--help			          Print usage instructions
--region		          The region
--instance-type		    The instance type for the ECS instance
--key			            The SSH key pair
--count			          The number of instances to launch
--security-group	    The "ID" of the security group to attach to the ECS instance
--subnet		          The "ID" of the subnet for the ECS instance to be launched in
--iam-role		        The "Name" of the IAM Role which must be attached to the instance
--cluster		          The Cluster Name
--user-data		        The path to a custom User Data script

Note: If you specify both a cluster and a user data location, the user data will take preference
