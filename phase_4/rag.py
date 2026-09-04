
from settings import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import logging

logger = logging.getLogger(__name__)



def load_vector_store():
    try:

        logger.info("Loading vector store from %s", settings.vector_store_path)
        embeddings=GoogleGenerativeAIEmbeddings(model=settings.embedding_model,
                                                google_api_key=settings.google_api_key)
        db=FAISS.load_local(settings.vector_store_path,
                            embeddings,
                            allow_dangerous_deserialization=True)
        logger.info("Vector store loaded successfully")
        return db
    
    except Exception:
        logger.exception("An unexpected error occurred while loading the vector store")
        raise


def initialize_rag():
        
        logger.info("Initializing RAG system")
        db=load_vector_store()
        retriever=db.as_retriever()
        llm=ChatGoogleGenerativeAI(model=settings.generation_model,
                                   api_key=settings.google_api_key,
                                            temperature=0
                
                                                )


        
            
        prompt=ChatPromptTemplate.from_messages([
                (
                    "system",
                            """ You are an Assistant.
                                Answer the question using only the provided context. If the answer isn't in the context, return :
                                {{
                                    "answer": "I don't have enough information to answer that."
                                }}

                                RULES:
                                1.give a simple,structured and comprehensive answer in not more than 5 sentences for only the questions you find answers fro the context.
                                2.The answer should naturally cover what, why, how, applications, examples, and future if the context contains that information.
                                3.Dont hallucinate or try to answer yourself for the questions that you cannot find answers from the context.
                                4.Do not use markdown
                                5.Do not return Json
                                
                                INPUT QUESTION EXAMPLE
                                "What is Machine Learning"
                                """
                ),
                ("human",
                """
                    CONTEXT:

                    {context}

                    USER QUESTION:

                    {input}
                """
                )
            ])

            
        document_chain=create_stuff_documents_chain(llm,prompt)


        retrieval_chain=create_retrieval_chain(
                    retriever,
                    document_chain
                )
        logger.info("retrieval chain initialized successfully")
        return retrieval_chain
    


def rag(question,retrieval_chain):
    try:
        logger.info("RAG invoked for question")
        response=retrieval_chain.invoke(
                    {
                        "input":question
                        
                    }
                )
        logger.info("RAG response generated successfully")
        return response['answer']
    
    except Exception:
        logger.exception("RAG query failed")
        raise
    
  