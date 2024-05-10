import requests
import boto3
session = boto3.Session()
aws_region = 'us-west-2'
ec2_client = session.client(service_name='ec2',region_name=aws_region)

def get_ecs_amis_releases_info(ami_ids):
    response = requests.get("https://api.github.com/repos/aws/amazon-ecs-ami/releases")
    response_json = response.json()
    releases_info = []
    ami_data = []
    for ami_id in ami_ids:
        ami_data.append({
            "name":get_ami_name_from_id(ami_id),
            "id": ami_id
        })
    for release in response_json:
        for ami in ami_data:
            if ami['name'] in release['body']:
                releases_info.append({"ami_id": ami['id'], 
                                      "ami_name":ami['name'],
                                      "details":release['body']})
                break
    return releases_info

def get_ami_name_from_id(ami_id):
    describe_image_response = ec2_client.describe_images(ImageIds=[ami_id])
    return describe_image_response['Images'][0]['Name']