from rag import initialize_rag,rag

def main():
    retrieval_chain=initialize_rag()
    while True:
        question=input("enter a question : ")
        if question.lower()=="exit":
            break
        try:
            response=rag(question,retrieval_chain)
            print(response)
        except Exception as e:
            print(type(e))
            raise
try:    
    main()
except FileNotFoundError as e:
    print(f"vector store file not found {e}")
except Exception as e:
    print(type(e))
    raise