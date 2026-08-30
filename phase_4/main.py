from rag import initialize_rag,rag
from schemas import Question,Answer,RebuildIndexResponse,HealthResponse
from fastapi import FastAPI,HTTPException
from build_index import build_index
from config import VECTOR_STORE_PATH
app=FastAPI()



if not VECTOR_STORE_PATH.exists():
    print("Vector store not found. Building index...")
    build_index()

retrieval_chain = initialize_rag()

@app.get("/")
def home():
    return {"message":"hello"}


@app.get("/health",response_model=HealthResponse)
def health():
    if retrieval_chain is None:
         return {"status":"fail",
                 "vector_store_loaded":False}
    
    return {"status":"ok",
            "vector_store_loaded":True
            }


@app.post("/ask",response_model=Answer)
def ask(request:Question):
    try:
        answer=rag(request.question,retrieval_chain)
        return {"answer":answer}
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail={"error":"vector store file not found"}
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error":str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error":str(e)}
        )

@app.post("/rebuild-index",response_model=RebuildIndexResponse)
def rebuild_index():
    
    global retrieval_chain

    try:
        
        db=build_index()
        retrieval_chain=initialize_rag()
        return {"status":"success",
                "message":"index build successfully"}
                 
    except FileNotFoundError:
            raise HTTPException(
                status_code=404,
                detail={"error":"vector store file not found"}
                )
    except ValueError as e:
            raise HTTPException(
                 status_code=400,
                 detail={"error":str(e)}
            )
    except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={"error":str(e)}
            )


