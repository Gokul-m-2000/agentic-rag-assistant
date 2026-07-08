"""
Entry point for the AI assistant pipeline.
Accepts a question, routes it through the agentic system,
and prints the final answer.

Usage: python main.py
"""
from router import route_question

que=input("Enter your question : ")
a=route_question(que)
if a:
    print(f"Final answer for the question : {que} is \n{a}")
else:
    print("Final answer is None")