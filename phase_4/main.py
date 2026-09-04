from rag import initialize_rag,rag
from schemas import Question,Answer,RebuildIndexResponse,HealthResponse
from fastapi import FastAPI,Request
from build_index import build_index,load_documents
import logging
from logging_config import configure_logging
import uuid
from request_context import request_id
import time 
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from exceptions import SourceDocumentNotFoundError,IndexBuildError
from fastapi import Depends
from auth import get_api_key
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from rate_limit import limiter



configure_logging()

logger=logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
     logger.info("Application startup beginning")

     app.state.retrieval_chain=initialize_rag()

     logger.info("RAG system initialized successfully")

     yield


     logger.info("Application shutdown beginning")





app=FastAPI(lifespan=lifespan)




app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler)


@app.exception_handler(SourceDocumentNotFoundError)
async def source_document_not_found_handler(
    request: Request,
    exc: SourceDocumentNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={"detail": "Source document not found"}
    )


@app.exception_handler(IndexBuildError)
async def index_build_error_handler(
    request: Request,
    exc: IndexBuildError
):
    return JSONResponse(
        status_code=500,
        content={"detail": "Failed to build index"}
    )



@app.exception_handler(Exception)
async def generaal_exception_handler(request:Request,exc:Exception):
    logger.exception("unexpected error!")
    return JSONResponse(
          status_code=500,
          content={"detail":"Internal server error"}
     )





@app.middleware("http")
async def request_id_middleware(request:Request,call_next):
    request_id_value=str(uuid.uuid4())

    request_id.set(request_id_value)
    timer=time.perf_counter()
    status_code=500
    try:
        response=await call_next(request)
        status_code=response.status_code
        return response
    finally:
        duration=time.perf_counter()-timer
        logger.info("Request completed : method=%s path=%s status_code=%d duration=%.4f seconds",
                            request.method,request.url.path,status_code,duration)
        
    
    








@app.get("/")
def home():
    logger.info("Home endpoint called")
    return {"message":"hello"}



@app.get("/health",response_model=HealthResponse)
def health(request:Request):
    logger.info("Health endpoint called")
    retrieval_chain = request.app.state.retrieval_chain
    if retrieval_chain is None:
         logger.error("Retrieval chain is not initialized")
         return {"status":"fail",
                 "vector_store_loaded":False}
    
    logger.info("Health check passed")
    return {"status":"ok",
            "vector_store_loaded":True
            }




@app.post("/ask",response_model=Answer)
@limiter.limit("5/minute")
def ask(question_request:Question,
        request:Request,
        api_key:str=Depends(get_api_key),
         ):
    
    logger.info("Ask endpoint called")
   
    retrieval_chain = request.app.state.retrieval_chain
    answer=rag(question_request.question,retrieval_chain)
    logger.info("answer received successfully")
    return {"answer":answer}
   




@app.post("/rebuild-index",response_model=RebuildIndexResponse)
def rebuild_index(request:Request):

    logger.info("Rebuild index endpoint called")

    documents=load_documents()
        
    build_index(documents)

    request.app.state.retrieval_chain = initialize_rag()
    logger.info("Index rebuilt successfully")
    return {"status":"success",
            "message":"index build successfully"}
                 
    