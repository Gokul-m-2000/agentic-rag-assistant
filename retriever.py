"""
Cosine similarity search over stored embeddings.
Manual implementation — no vector DB used.
"""

import json
import numpy as np
from embedder import get_embedding_text
from config import EMBEDDINGS_FILE


def cosine_similarity(vec_a,vec_b):
    try :
        if vec_a is not None and  vec_b is not None:
            if np.shape(vec_a)==np.shape(vec_b):
                if np.linalg.norm(vec_a)!=0 or np.linalg.norm(vec_b)!=0:
                    similarity=(np.dot(vec_a,vec_b))/(np.linalg.norm(vec_a)*np.linalg.norm(vec_b))
                    return similarity
                else:
                    raise ValueError("division by zero not possible")
            else:
                raise ValueError("shape mismatch ! ")
        else:
            raise ValueError("vec_a or vec_b cannot be empty")
    except Exception as e:
        print(e)
        return None
    


def retreive_top_chunks(question,top_n=3):
    question=question.strip()
    similarity_list=[]
    failed_similarity_list=[]
    
    if question:
            q_embed=get_embedding_text(question)
            if q_embed is not None:
                try:
                    with open(EMBEDDINGS_FILE,"r") as f4:
                            data=json.load(f4)
                except FileNotFoundError as e:
                    print("file not found , {e}")
                    return None
                except json.JSONDecodeError as e:
                    print(f"json loading error , {e}")
                    return None
                except Exception as e:
                    print(e)
                    return None
                if data:
                    for i in range(len(data)):
                        retreived_vector=data[i]["embeddings"]
                        similarity_score=cosine_similarity(q_embed,retreived_vector)
                        if similarity_score is not None:
                            similarity_d={'index':i,'score':similarity_score}
                            similarity_list.append(similarity_d)
                        else:
                            failed_similarity_list.append({'index':i,'error':"None returned from cosine function "})
                    print(f"Length of similarity list {len(similarity_list)}")
                    print(f"Length of failed similarity list {len(failed_similarity_list)}")
                    if similarity_list:
                        sorted_similarity_index=[x['index'] for x in sorted(similarity_list,key=lambda x: x['score'],reverse=True)]
                        top_chunk_n=[]
                        for j in sorted_similarity_index[:top_n]:
                            top_chunk_n.append(data[j]["text"])
                        return top_chunk_n
                    else:
                        raise ValueError("similarity list empty ! ")
                else:
                        raise ValueError("empty data returned")
            else:
                raise ValueError("Question not embedded")

    else:
            raise ValueError("Question is empty ! ")