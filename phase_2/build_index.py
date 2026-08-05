"""
One-time script: reads doc.txt, chunks it, embeds all chunks,
and saves to embeddings.json.
Run this once before using the main pipeline.
Usage: python build_index.py
"""
import json
from chunker import chunk_text
from embedder import get_embedding_text
from config import CHUNK_SIZE, OVERLAP,api_key,DOC_FILE,EMBEDDINGS_FILE



with open(DOC_FILE,'r')as f:
    character=f.read()

    chunked=chunk_text(CHUNK_SIZE, OVERLAP,character)
    if chunked:
            embeddings_list=[]
            Log_Not_embedded=[]
            print(f"Chunking done ,Total chunks {len(chunked)}")
            print(f"chunk 2nd last \n{chunked[-2]}")
            print(f"chunk last \n{chunked[-1]}")
            print("embedding is starting")
            for i in range(len(chunked)):

                embed=get_embedding_text(chunked[i],api_key)
                if embed is not None:
                    embeddings_dict={"text":chunked[i],"embeddings":embed}
                    embeddings_list.append(embeddings_dict)
                else:
                    Log_Not_embedded.append(chunked[i])

            print(f"Total embedded chunks {len(embeddings_list)}")
            print(f"Failed embedded chunks {len(Log_Not_embedded)}")
            if embeddings_list:
                with open(EMBEDDINGS_FILE,"w")as f2:
                    json.dump(embeddings_list,f2)
                    print("saved as json file")
            else:
                print("embedding list empty")
           
    else:
            print("chunk variable empty, check your chunk function")