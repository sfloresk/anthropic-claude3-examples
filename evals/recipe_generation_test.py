import boto3
import pytest
import json

model_id ='anthropic.claude-3-sonnet-20240229-v1:0' 
session = boto3.Session()
aws_region = 'us-east-1'
bedrock_client = session.client(service_name='bedrock-runtime', region_name=aws_region)

system_prompt = """
You are a chef that creates recipes
"""

base_user_prompt = """
Create a recipe for the followind dish following this rules
1. Include a description of the dish
2. Include a list of ingredients
3. Include a list of steps to create the dish
Now, create a recipe for this dish. Skip the preamble or postamble, go straight to the answer
<dish></dish>
"""

scores = []

@pytest.fixture(scope="session")
def scores_ft(request):
    print(f"""Using prompt template:
          {base_user_prompt}""")
    
    global scores 
    print("\nSetting up resources...")
    yield scores
    print("\n======== Report ========")
    
    for item in scores:
        print("========")
        print(f'======== Results for {item["dish"]}')
        print(f'======== Model response: {item["response"]}')
        print(f'======== Score percent: {item["score_percent"]}')
        
    

@pytest.mark.parametrize("dish", [
    ("cornmeal"),
    ("lasagna"),
    #("chocolate cake"),
    #("flan"),
])

def test_dish(dish,scores_ft):
    print(f"\n=====")
    print(f"Testing recipe: {dish}")
    request_prompt = base_user_prompt.replace("<dish></dish>",f"<dish>{dish}</dish>")
    request_body = { 
        "anthropic_version": "bedrock-2023-05-31",
        'max_tokens': 2048,
        "system": system_prompt,
        "temperature":0,
        "stop_sequences":[],
    	"messages": [
            {
            "role": "user",
            "content": [
                    {
                    "type": "text",
                    "text": request_prompt
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
    response_text = response_body['content'][0]['text'].lower()

    # init scores
    score = 0
    max_score = 3

    # According to keywords found, increase score
    if dish.lower() in response_text:
        score +=1
    if "steps" in response_text:
        score +=1
    if "ingredients" in response_text:
        score +=1
    
    relative_score = int(score/max_score * 100)

    scores_ft.append({
        "dish": dish,
        "response": response_text,
        "score_percent": f'{relative_score}%'
    })
    
    assert(relative_score >= 75)

