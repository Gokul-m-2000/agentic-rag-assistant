from config import GENERATION_MODEL,VECTOR_STORE_PATH,EMBEDDING_MODEL
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain


def load_vectore_store():
    embeddings=GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    db=FAISS.load_local(VECTOR_STORE_PATH,
                        embeddings,
                        allow_dangerous_deserialization=True)
    return db


def initialize_rag():
    
    
    db=load_vectore_store()
    retreiver=db.as_retriever()
    llm=ChatGoogleGenerativeAI(model=GENERATION_MODEL,
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
                retreiver,
                document_chain
            )
    return retrieval_chain



def rag(question,retrieval_chain):
    response=retrieval_chain.invoke(
                {
                    "input":question
                    
                }
            )
    return response['answer']
    
  