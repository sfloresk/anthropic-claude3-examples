import boto3
import pytest
import json

model_id ='anthropic.claude-3-sonnet-20240229-v1:0' 
session = boto3.Session()
aws_region = 'us-west-2'
bedrock_client = session.client(service_name='bedrock-runtime', region_name=aws_region)


if __name__ == "__main__":
    model_name = "Claude 3"
    request_body = { 
        "anthropic_version": "bedrock-2023-05-31",
        'max_tokens': 512,
        "system": "You are an assistant that helps humans to be more productive.",
        "temperature":0,
        "stop_sequences":[],
    	"messages": [
            {
            "role": "user",
            "content": [
                    {
                    "type": "text",
                    "text": f"""List best practices for prompts for the following foundational model in <best_practices></best_practices> tags. 
                    For example 
                    <best_practices>
                    1. this a best practice
                    2. this another best practice
                    </best_practices>
                    Think step by step using <thinking></thinking> tags 
                    Now list the best practices for the model 
                    <model>{model_name}</model>"""
                    }
                ]
            },{
            "role": "assistant",
            "content": [
                    {
                    "type": "text",
                    "text": """<thinking>"""
                    }
                ]
            }
        ]
    }
    
    response = bedrock_client.invoke_model_with_response_stream(
        body=json.dumps(request_body),
        modelId=model_id, 
        accept='application/json', 
        contentType='application/json'
    )
    for event in response.get("body"):
        response = json.loads(event['chunk']['bytes'].decode())
        
        if response['type'] == 'content_block_start':
            print(response['content_block']['text'],end='')
        elif response['type'] == 'content_block_delta':
            print(response['delta']['text'],end='')

