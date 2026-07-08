"""
External tools available to the agentic router:
- calculator: evaluates arithmetic expressions safely
"""

import wikipedia


def calculator(expression):
    print(f"Initializing calculator for {expression}")
    try:
        
            allowed=set('0123456789+-*/.%()')
            if not all(c in allowed for c in expression):
                raise ValueError("unallowed character in expression")
    
            result=eval(expression)
            return result
    except ZeroDivisionError:
            print("Error: Division by zero is not allowed.")
            return "zero division not possible"
    except Exception as e:
            print(f"Error: {e}")
            return None


def wikipedia_search(query):
      try:
        if query:
                print(f'initializing wikipedia search for :{query}')
                wiki_answer=wikipedia.summary(query)
                if wiki_answer:
                    print(f"returning answer from wiki : {wiki_answer}")
                    return wiki_answer
                else:
                    raise ValueError("No results or empty result from wiki")
      except Exception as e:
            print(f"exception occured ,  {e}")
            return None
