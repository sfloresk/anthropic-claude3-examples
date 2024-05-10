import boto3
import pytest
import json

model_id ='anthropic.claude-3-sonnet-20240229-v1:0' 
session = boto3.Session()
aws_region = 'us-west-2'
bedrock_client = session.client(service_name='bedrock-runtime', region_name=aws_region)


if __name__ == "__main__":
    
    request_body = { 
        "anthropic_version": "bedrock-2023-05-31",
        'max_tokens': 512,
        "system": "You are an assistant that helps humans to be more productive",
        "temperature":0,
        "stop_sequences":[],
    	"messages": [
            {
            "role": "user",
            "content": [
                    {
                    "type": "text",
                    "text": "Hello, world!"
                    }
                ]
            },
            {
            "role": "assistant",
            "content": [
                    {
                    "type": "text",
                    "text": "Hi there, how can I help you?"
                    }
                ]
            },
            {
            "role": "user",
            "content": [
                    {
                    "type": "text",
                    "text": "I need to create good prompts for a foundational model"
                    }
                ]
            }
        ]
    }
    response = bedrock_client.invoke_model(
        body=json.dumps(request_body), 
        modelId=model_id, 
        accept='application/json', 
        contentType='application/json'
    )

    body = response.get('body').read().decode('utf-8')
    response_body = json.loads(body)
    response_text = response_body['content'][0]['text']
    
    print(response_text)

