import boto3
import pytest
import json
import httpx
import base64

model_id ='anthropic.claude-3-sonnet-20240229-v1:0' 
session = boto3.Session()
aws_region = 'us-west-2'
bedrock_client = session.client(service_name='bedrock-runtime', region_name=aws_region)


if __name__ == "__main__":
    image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
    image1_data = base64.b64encode(httpx.get(image1_url).content).decode("utf-8")

    image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
    image2_data = base64.b64encode(httpx.get(image2_url).content).decode("utf-8")

    model_name = "Claude 3"
    request_body = { 
        "anthropic_version": "bedrock-2023-05-31",
        'max_tokens': 1024,
        "system": "You are an image recognition AI assistant that identify differences between pictures",
        "temperature":0,
        "stop_sequences":["</result>"],
    	"messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Image 1:"
                        },
                        {
                                  "type": "image",
                                  "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image1_data
                                  }
                        },
                        {
                            "type": "text",
                            "text": "Image 2:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image2_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "How are these images different?"
                        }
                    ]
                },{
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "<result>"
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

