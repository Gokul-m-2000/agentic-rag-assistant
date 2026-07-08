"""
LLM-as-judge evaluation pipeline for the RAG system.
Loads run_results.json, judges each answer, saves eval_results.json,
and appends a summary line to eval_log.txt.

Usage: python evaluator.py
"""

import json
from datetime import datetime
from generator import api_connect
from config import RUN_RESULTS_FILE,EVAL_RESULTS_FILE,EVAL_LOG_FILE

def judge(question,expected_answer,actual_answer,check_type):
    system_prompt=f"""  you are an evaluator,not an answerer.
                        you will receive question, expected answer, actual answer and check type as context.


                        RULES:
                        1.evaluate the actual answer based on the expected answer and check_type and give veredict and reason
                        2.Use only provided information to give veredict and reason, do not hallucinate or fabricate any information.
                        3.strictly follow the rules and Must return only valid JSON in the shape below(output format) — no preamble, no markdown fences.


                        CHECK TYPE
                        1.in_scope:check whether actual_answer covers the key facts in expected_answer, even if worded differently.
                          Minor omissions are acceptable; factual contradictions or hallucinated claims not in the expected answer are failures.
                        2.out_of_scope: check whether actual_answer is a refusal (says it doesn't have information, or equivalent).
                          If the system fabricated an answer instead of refusing, that's a failure.

                        OUTPUT FORMAT:
                        {{
                            
                            "verdict": "pass" or "fail",
                            "reason": "one sentence explaining why",
                            "check_type": "in_scope" or "out_of_scope"

                        }}
                        """

    user_question=f"""question :{question},
                      expected answer:{expected_answer},
                      actual answer:{actual_answer},
                      check type:{check_type}
                      """
    verdict=api_connect(system_prompt,user_question)
    if verdict is not None:
        print(f"api connect returned a {type(verdict)}")
        return verdict
    else:
        print(f"api connect returned None")
        return None



log=[]
eval_list=[]
try:
    with open(RUN_RESULTS_FILE,"r")as f:
        data=json.load(f)
        print(f"run_results.json file opened and loaded , total test cases {len(data)}")
    if data:
        total = 0

        in_scope_total = 0
        in_scope_pass = 0

        out_scope_total = 0
        out_scope_pass = 0
        for r in data:
            question=r["question"]
            expected_answer=r["expected answer"]
            actual_answer=r["actual answer"]
            if expected_answer=="\"I don't have enough information to answer that.\" (this is NOT covered in the source document)":
                check_type="out_of_scope"
                out_scope_total+=1
            else:
                check_type="in_scope"
                in_scope_total+=1
            total += 1
            eval_r=judge(question,expected_answer,actual_answer,check_type)
            if eval_r:
                print(f"evalution result received for this question : {question}")
                eval_dict={"question":question,"expected answer":expected_answer,"actual answer":actual_answer,"check type":check_type,"evaluation":eval_r}
                print(f"eval_dict formed")
                eval_list.append(eval_dict)
                print(f"eval_list formed")
                if eval_r["verdict"] == "pass":
                    if check_type == "in_scope":
                        in_scope_pass += 1
                    elif check_type == "out_of_scope":
                        out_scope_pass += 1
            else:
                print(f"evalution result not received for this question : {question}")
        if eval_list:    
            print("trying to open evel_results.json file to save eval_list")
            with open(EVAL_RESULTS_FILE,"w") as ev:
                json.dump(eval_list,ev,indent=4,ensure_ascii=False)
                print(" eval_list to eval_results.json file done")
                print(f"Total test cases evaluated : {total}")
            print("Trying to open eval_log.txt file to save log")
            with open(EVAL_LOG_FILE,"a") as f1:
                f1.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S') } | Total : {total} | In_scope_pass: {in_scope_pass}/{in_scope_total} | Out_of_scope_pass: {out_scope_pass}/{out_scope_total} | overall:{(in_scope_pass+out_scope_pass)}/{total} | percentage : {(in_scope_pass+out_scope_pass)/total*100:.1f}%\n")
                print("eval_log.txt file updated")
        else:
            raise ValueError("eval_list empty , check your eval_list formation")
                
    else:
        raise ValueError("run_results.json file empty , check your run_results.json file")

except json.JSONDecodeError as e:
    print(f"Json error ,{e}")
except Exception as e:
    print(f"error , {e}")
