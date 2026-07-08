"""
Handles all calls to Gemini's generateContent endpoint.
Used for both RAG answer generation and agentic synthesis.
"""

from config import api_key, GENERATION_MODEL
import json
import time
import requests

def api_connect(system_prompt,user_question,api_key=api_key):
    try:
        if api_key and system_prompt and user_question:
            
            url= f"https://generativelanguage.googleapis.com/v1beta/models/{GENERATION_MODEL}:generateContent"
            my_header={
                "x-goog-api-key":api_key,
                "content-type":"application/json"
            }
            system_prompt=system_prompt
            user_question_to_analyse=user_question
            payload={
                "systemInstruction":{
                    "parts":[{"text":system_prompt}]
                },
                "contents":[{
                    "role":"user",
                    "parts":[{"text":user_question_to_analyse}]
                }]

            }

            
           
            response=requests.post(url,json=payload,headers=my_header)
            limit=0
            delay=0
            while response.status_code==429 and limit<3:
                    delay_s=response.json()['error']['details'][2]['retryDelay']
                    delay_in_response=int(delay_s.rstrip('s'))
                    t_delay=delay_in_response+delay
                    print(f"waiting for  {t_delay} seconds until next try ...")
                    time.sleep(t_delay)
                    response=requests.post(url,json=payload,headers=my_header)
                    limit+=1
                    delay+=5

            if response.status_code!=200:
                    print(f"Faulty response, status code: {response.status_code} ")
                    raise ValueError(f"response text {response.text}")
                
            text=response.json()['candidates'][0]['content']['parts'][0]['text']
              
                
            new_text=json.loads(text.replace("```json","").replace("```",""))
    
            return new_text
                
                    
            
        else:
            raise ValueError("api key,question and system prompt cannot be empty ! ")
    
    except requests.exceptions.Timeout as e:
        print(f"Request Time out error !{e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error !{e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"request error !{e}")
        return None
    except json.JSONDecodeError as e:
        print(f"print json decode error ,{e}")
        print(type(new_text))
        return None
    except Exception as e:
        print(f"Error ! {e}")
        return None
    



def ai_assistant(top_chunk,question):
    top_chunk=top_chunk
    system_prompt=f"""  You are an Assistant.
                        Answer the question using ONLY the context below. If the answer isn't in the context, return :
                        {{
                            "answer": "I don't have enough information to answer that."
                        }}
                        CONTEXT:

                        {top_chunk[0]}

                        {top_chunk[1]}

                        {top_chunk[2]}

                        RULES:
                        1.give a simple,structured and comprehensive answer in not more than 5 sentences for only the questions you find answers fro the context.
                        2.The answer should naturally cover what, why, how, applications, examples, and future if the context contains that information.
                        3.Dont hallucinate or try to answer yourself for the questions that you cannot find answers from the context.
                        3.Should strictly return the answer in a valid JSON format as the example given below
                        
                        INPUT QUESTION EXAMPLE
                        "What is Machine Learning"
                        OUTPUT FORMAT
                        {{
                          "answer": ""
                        }}
                        """
    user_question=question
    answer=api_connect(system_prompt,user_question)
    if answer is not None:
        print(f"returning only text from the answer(ai assistant) ")
        return answer['answer']
        
    else:
        print("api connect returned None")
        return None