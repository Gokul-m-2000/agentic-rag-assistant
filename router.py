"""
Agentic router: decides which tools to use for a given question,
executes them, and synthesizes a final answer.
"""

from generator import api_connect,ai_assistant
from retriever import retreive_top_chunks
from tools import calculator,wikipedia_search



def route_question(que):
    system_prompt_router=f"""You are a router and reasoner.
                      you will get questions and tools that are available to use.

                      TOOLS:
                      1.rag :for questions about topics covered in the knowledge base (AI history, concepts, applications, risks)
                      2.calculator :FOR CALCULATIONS
                      3.wikipedia :FOR EXTERNAL OR CURRENT INFORMATION WHICH IS NOT IN RAG

                      RULES:
                      1.Analyse the question and reason what tools to use for the question.
                      2.If the tool to be used is calculator ,extract the expression from question and return it in the expression section.
                      3.expression should be returned in a list as given in the output format
                      4.if the tool is wipedia_search,return the question optimized for wipedia search in the wikipedia_query section.
                      5.Return only the most relevant Wikipedia page title or entity name. Remove question words like "what", "who", "right now", "tell me", etc.
                      6.You only have to sent back relavent tools and its details that is needed for the question,don't need to send other tools(if rag is the only tool needeed,then only sent 
                      "tools":[
                            {{
                            "name":"rag",
                            "query":"general intelligence"
                            }}]
                      6.if the expresssion contains '^' then replace it with '**' for power operation and return the expression in the expression section.
                      8.Should strictly follow the rules and return the answer in a valid JSON format as the example given below.

                      INPUT QUESTION EXAMPLE:
                      "What is Machine Learning and what is 5+6 and 8-9 and who is the current president of america"

                      OUTPUT FORMAT:
                      {{
                        "tools":[
                            {{
                            "name":"rag",
                            "query":"general intelligence"
                            }},
                            {{
                            "name":"wikipedia",
                            "query":"President of america"
                            }},
                            {{
                            "name":"calculator",
                            "expression":["5+6","8-9"]
                            }}
                        ]
                      }}

                    """
    

    
    main_answer=[]
    calc_list=[]

    user_question=que
    response_route=api_connect(system_prompt_router,user_question)
    if response_route is not None:
        for tool in response_route['tools']:
            print(f"tool :{tool}")
            if tool['name']=="rag":
                question=tool['query']
                top_ch=retreive_top_chunks(question)
                if top_ch:
                    ai_answer=ai_assistant(top_ch,question)
                    if ai_answer is not None:
                        rag_answer_dict={"rag_answer":ai_answer}
                        main_answer.append(rag_answer_dict)
                        print(f"rag answer appended to main,length of main_answr : {len(main_answer)}")
                        print(f"Answer from RAG received for: {question}, answer :{ai_answer}")
                    else:
                        main_answer.append({"rag_answer":None})
                        print("Answer from RAG is None")
                else:
                    print("Top chunks from RAG is None")
            elif tool['name']=="calculator":
                expression=tool['expression']
                for ex in expression:
                    ex=ex.replace(" ","")
                    if ex:
                        calc_answer=calculator(ex)
                        if calc_answer:
                            calc_dict={"expression":ex,"calc_answer":calc_answer}
                            calc_list.append(calc_dict)
                        else:
                            calc_dict={"expression":ex,"calc_answer":None}
                            calc_list.append(calc_dict)
                if calc_list:
                    main_answer.append(calc_list)
                else:
                    main_answer.append({"calculator_answer":None})
            elif tool['name']=="wikipedia":
                wiki_query=tool['query']
                print(f"wikipedia query recived from llm : {wiki_query}")
                print(f"type of wiki query :{type(wiki_query)}")
                summary=wikipedia_search(wiki_query)
                if summary is not None:
                    main_answer.append({"wikipedia_answer":summary})
                else:
                    main_answer.append({"wikipedia_answer":summary})
                    print("Answer from wikipedia is None")
                   
            
             
        if main_answer:
            print(f"main answer sending to llm : {main_answer}")
            system_prompt_final=f"""You are an Assistant.
                                    Answer the question using ONLY the context below. If the answers isn't in the context, return :
                                    {{
                                        "answer": "I don't have enough information to answer that."
                                    }}
                                        CONTEXT:

                                    {main_answer}

                                
                                    RULES:
                                    
                                    1.The answer should be direct or explanatory as per question and only if the context contains that information.
                                    2.give a simple,structured and comprehensive answer for explanatory questions in not more than 7 sentences.
                                    3.Question may contain multiple questions, answer all the questions in the context if the context contains that information.
                                    4.Incase where in the context gives None or If the answer is not in the context for a specific question, return the refusal message for that question only and return the answers to the other questions that you received.
                                    5.Explicitly specify the answers with the related question part so that user can understand which answer is for which question.
                                    6.Context is going to be a list of answers from different tools, so you need to reason and combine the answers in a structured way.
                                    7.Context from calculator is in calculator_answer key, context from RAG is in rag_answer key and context from wikipedia is in wikipedia_answer key.
                                    8.answer all questions and combine them in a single response. 
                                    9.Should strictly return the answer in a valid JSON format as the example given below
                        
                                    INPUT QUESTION EXAMPLE
                                    "What is Machine Learning and what is 5+6 and 8-9"
                                    OUTPUT FORMAT
                                    {{
                                            "answer": ""
                                    }}

                                    """
                
            response_final=api_connect(system_prompt_final,user_question)
            if response_final is not None:
                print(f"returning only text from the answer(api_connect) ")
                return response_final['answer']
            else:
                print("api connect returned None")
                return None
            