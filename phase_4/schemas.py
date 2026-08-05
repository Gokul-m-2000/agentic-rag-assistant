from pydantic import BaseModel,Field



class Question(BaseModel):
    question:str=Field(
        min_length=1,
        max_length=500
        )


class Answer(BaseModel):
    answer:str


class RebuildIndexResponse(BaseModel):
    status:str
    message:str


class HealthResponse(BaseModel):
    status:str
    vector_store_loaded:bool
   
