"""
Generates embeddings for text chunks using Gemini's embedContent API.
Saves results to embeddings.json for reuse across sessions.
"""


import requests
import json
import logging
import http.client
from config import api_key,EMBEDDING_MODEL,OUTPUT_DIMENSIONALITY





# http.client.HTTPConnection.debuglevel=1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log=logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate=True






def get_embedding_text(chunk,api_key=api_key):

    url=f"https://generativelanguage.googleapis.com/v1beta/models/{EMBEDDING_MODEL}:embedContent"

    my_header={
        "x-goog-api-key":api_key,
        "content-type":"application/json"
    }

    payload={"model":f"models/{EMBEDDING_MODEL}",
                "content":{
                    "parts":[
                        {
                        "text":chunk
                        }
                    ]
                },
                "outputDimensionality": OUTPUT_DIMENSIONALITY
    }

    try:
        response=requests.post(url,json=payload,headers=my_header)
        response.raise_for_status()
        try:
            data=response.json()
            vector=data['embedding']['values']
            print(f"Success , data  is : {len(vector)} dimensions")
            return vector
        except json.JSONDecodeError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None
    except requests.exceptions.Timeout as e:
        print(f"timeout{e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"connection{e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"request exception{e}")
        return None
    except Exception as e:
        print(e)
        return None
