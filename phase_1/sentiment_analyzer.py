from dotenv import load_dotenv
import os
import requests
import json
import logging
import http.client



load_dotenv()


# http.client.HTTPConnection.debuglevel=1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log=logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate=True



api_key=os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Api key is missing")

url= f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
my_header={
    "x-goog-api-key":api_key,
    "content-type":"application/json"
}
system_prompt="""You are a proffesional product review analyst.
                Your job is to review the product reviews and give a structured summary of the reviews in 1 sentences.

                RULES:
                1.provide a sentimental analysis(positive,negative,neutral,mixed)
                2.Details of the Entities,products,Oragnizations etc.
                3.Should strictly return the review in a valid JSON format with the exact shape as the example given below
                
                INPUT EXAMPLE
                "the product was ok for the price.not great,customer service was terrible,but reached somewhat on time ,i won't buy again unless the price goes low"
                OUTPUT FORMAT
                {
                "sentiment": "positive | negative | neutral | mixed",
                "entities": ["list", "of", "names/products/orgs mentioned"],
                "summary": "one sentence summary,not more than 20 words"
                }
                """
user_review_to_analyse="I absolutely love my new Sony headphones! The noise cancellation is unreal, though the battery life could be a little better. Overall, worth the $300."
payload={
    "systemInstruction":{
        "parts":[{"text":system_prompt}]
    },
    "contents":[{
        "role":"user",
        "parts":[{"text":user_review_to_analyse}]
    }]

}

try:

    response=requests.post(url,json=payload,headers=my_header)
    if response.status_code!=200:
        print(f"Faulty response, status code: {response.status_code} ")
        print(f"response text {response.text}")
        exit()
    text=response.json()['candidates'][0]['content']['parts'][0]['text']
    
    try:
        new_text=json.loads(text.replace("```json","").replace("```",""))
       
        d=json.dumps(new_text,indent=2)
        print(d)
        print(type(d))
        print(repr(d))
    except json.JSONDecodeError as e:
        print(f"print json decode error ,{e}")
    except Exception as e:
         print(f"error ! {e}")
        
except requests.exceptions.Timeout as e:
    print(f"Request Time out error !{e}")
except requests.exceptions.ConnectionError as e:
        print(f"Connection error !{e}")
except requests.exceptions.RequestException as e:
        print(f"request error !{e}")
except Exception as e:
     print(f"Error ! {e}")


