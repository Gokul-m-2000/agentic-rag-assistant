


import json
from pathlib import Path
import copy
from retriever import retreive_top_chunks
from generator import ai_assistant
from config import GOLD_TEST_FILE,RUN_RESULTS_FILE




try:
    test=[]
    print("trying to open test file ..")
    with open(GOLD_TEST_FILE,"r") as gold:
        test=json.load(gold)
        print("test file opened and loaded..")
except json.JSONDecodeError as e:
    print(f"Json error ,{e}")
except Exception as e:
    print(e)

run_results=[]
results=[]
if test:
    print(f"Total test cases {len(test)}")
    file=RUN_RESULTS_FILE
    if file.exists():
        if file.stat().st_size>0:
            try:
                print("Results file exists and trying to open  it ..")
                with open(RUN_RESULTS_FILE,"r")as result:
                    results=json.load(result)
                    print("file loaded ..")
                    print(f"length of result : {len(results)}")
            except json.JSONDecodeError as e:
                print(f"json error ,{e}")
            except Exception as e:
                print(f"error , {e}")
        else:
            print("file empty")
    else:
        print("file does not exist , creating new file")
    if results:
        results_copy=copy.deepcopy(results)
          
        lookup_dict={r["question"]:r for r in results}
        for q in test:
            question=q['question']
            answer=q['answer']
            if question in lookup_dict:
                    r=lookup_dict[question]
                    if not r["retreived chunks"]:
                        print(f"chunks not available for this {question}")
                        top_ch=retreive_top_chunks(question)
                        if top_ch:
                            r["retreived chunks"]=top_ch
                            print(f"top chunks received for this: {question}")
                        else:
                            print(f"Chunks not recived for {question},empty list ")
                        
                    if not r["actual answer"] :
                        print(f"actual answer not available for this {question}")
                        if r["retreived chunks"] :
                            ai_answer=ai_assistant(r["retreived chunks"],question)
                            if ai_answer is not None:
                                r["actual answer"]=ai_answer
                                print(f"answer recived for this: {question}")
                            else:
                                print(f"answer received empty for {question}")
                        else:
                            print(f"no chunks available for {question}")
                    
            else:
                    top_ch=retreive_top_chunks(question)
                    print(f"top chunks received for this: {question}")
                    if top_ch:
                        ai_answer=ai_assistant(top_ch,question)
                        print(f"answer recived for this: {question}")
                        if ai_answer is not None:
                            results_dict={"question":question,"expected answer":answer,"actual answer":ai_answer,"retreived chunks":top_ch}
                            results.append(results_dict)
                            lookup_dict[question]=results_dict
                        else:
                            print(f"answer receoved empty for {question}")
                    else:
                        print("top chunks not received ,list empty")
                    print(len(results))
        
        if results==results_copy:
                print("No modifications done")
                # exit()
        else:
            with open(RUN_RESULTS_FILE,"w")as new:
                json.dump(results,new,indent=4,ensure_ascii=False)
                print("file changed and saved ! ")


                           
    else:
        for q in test:
            question=q['question']
            answer=q['answer']
            top_ch=retreive_top_chunks(question)
            print(f"top chunks received for this: {question}")
            if top_ch:
                ai_answer=ai_assistant(top_ch,question)
                print(f"answer recived for this: {question}")
                if ai_answer is not None:
                    results_dict={"question":question,"expected answer":answer,"actual answer":ai_answer,"retreived chunks":top_ch}
                    run_results.append(results_dict)
                else:
                    print(f"answer receoved empty for {question}")
            else:
                print("top chunks not received ,list empty")
            print(len(run_results))

        if run_results:
            print("run_results opening")
            with open(RUN_RESULTS_FILE,"w")as test:
                json.dump(run_results,test,indent=4,ensure_ascii=False)
        else:
            raise ValueError("run results error or empty")
else:
    print("test cases empty , check your gold_test.json file")
