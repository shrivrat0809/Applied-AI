import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

if not api_key :
    print("API key not found")
    os.exit(0)

client = Groq(api_key=api_key)
model = "llama-3.3-70b-versatile"

# create tools
def get_product_price(product):
    _product = product.lower()
    if _product == "iphone 17" :
        return 15000
    elif _product == "iphone 15":
        return 10000
    else: return 0

def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calculator error!"

tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}

sytem_prompt = """
you are a shopping assistant.

You have the following tools:
get_product_price(product)
calculator(expression)

# IMPORTANT
call these tools exactly in this format:
Action: get_product_price("iPhone 17")
Action: calculator("5000 - 1000")

Never write:
get_product_price(product="iPhone 17")

Never write:
calculator(expression="5000 - 1000")

Always follow these rules:
1. First decide what to do next.
2. Look up to all the tools available to you.
3. choose one tool at a time, choosen tool should be of the most suitable for thecurrent job.
4. CALL the tool.
5. After writing an Action, STOP immediately
6. Never guess or invent a tool result.
7. Wait until you receive an Observation.
8. Then decide your next action.
9. When the task is complete, give the Final Answer.

Output Format: 
Thought: What you need to do
Action:
Tool: tool_name
Input: argument

When finished:

Final Answer: your answer
"""

def run_agent(question):
    messages = [
        {
            "role": "system",
            "content": sytem_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(5):

        print("\n------------------")
        print("STEP", step + 1)
        print("------------------")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0
        )

        answer = response.choices[0].message.content

        print(answer)
        # agent finished
        if "Final Answer" in answer:
            break
        tool_name = ""
        tool_input = ""
        for line in answer.splitlines():
            if line.startswith("Tool:"):
                tool_name = line.split(":", 1)[1].strip()

            elif line.startswith("Input:"):
                tool_input = line.split(":", 1)[1].strip()

        if tool_name in tools:
            tool = tools[tool_name]
            observation = tool(tool_input)
        else:
            observation = "tool not found"

        print("observation:",observation)

        messages.append({
            "role": "assistant",
            "content": answer
        })

        messages.append({
            "role": "user",
            "content":"Observation: " + str(observation)
        })
        sleep(5)



user_prompt = """
I have 15000 rupees. What is the price of an iphone 17?
and how much money will I have left?
"""

run_agent(user_prompt)