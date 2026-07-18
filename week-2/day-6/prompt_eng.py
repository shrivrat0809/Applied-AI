import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)
model = "llama-3.3-70b-versatile"

def llm_res(prompt):
    message = {
        "role": "user",
        "content": prompt
    }
    messages = [message]
    responce = client.chat.completions.create(model = model, messages = messages)
    ans = responce.choices[0].message.content
    return ans

bad_prompt = """
This is a user prompt:
My lapton is not working. Classify this issue
"""

# print(llm_res(bad_prompt))
########## responce ##########
# Specifically, it falls under the category of "Computer/Laptop Malfunction" since the laptop is not working at all.

# If you'd like to troubleshoot or get more specific help, please provide more details about the issue, such as:

# * What happens when you try to turn it on?
# * Are there any error messages or beeps?
# * Have you recently installed any new software or hardware?
# * Has the laptop been exposed to any physical damage or water?

# This will help me narrow down the possible causes and provide more targeted assistance.

prompt_with_role = """
#ROLE
you are a customer support assistant for a mobile/laptop company.
This is a user prompt:
My lapton is not working. Classify this issue
"""
# print(llm_res(prompt_with_role))
# **"Laptop Not Turning On" or "Laptop Not Functioning"**

# Could you please provide more details about the issue you're experiencing? For example:

# * What happens when you try to turn on your laptop?
# * Are there any error messages or beeps?
# * Have you tried charging the laptop or using a different power source?
# * Have you recently installed any new software or hardware?

# This will help me better understand the problem and provide a more accurate

prompt_with_task = """
#ROLE
you are a customer support assistant for a mobile/laptop company.
#TASK
you have to look into the issue and CLASSIFY the issue into Technical, Billing, Return
This is a user prompt:
My lapton is not working. Classify this issue
"""
# print(llm_res(prompt_with_task))
# Based on the information provided, I would clI'd be happy to help
#  you with your issue. Based on your prompt "My lapton is not working", 
# I would classify this issue as **Technical**, as it appears to be related to the functioning of your laptop. 
# Can you please provide more details about the issue you're experiencing

prompt_with_constraints = """
#ROLE
you are a customer support assistant for a mobile/laptop company.
#TASK
you have to look into the issue and CLASSIFY the issue into Technical, Billing, Return
#CONSTRAINTS
you have to classify the every issue only from the issues specified in the TASK
This is a user prompt:
my girlfriend need money
"""
# print(llm_res(prompt_with_constraints))
# I'm happy to help you, but I have to classify your issue according to our guidelines. Based on what you've told me, "my girlfriend need money" doesn't seem to be related to a technical problem with a mobile or laptop, nor is it a billing or return issue.

# However, I must choose from the given options, and since it's not related to a technical problem or a return, I would say it's closest to a "Billing" issue, but only in the sense that it's a financial matter. Nevertheless, please note that this is not a billing issue related to our company's products or services.

# Classification: Billing

prompt_with_output_format = """
#ROLE
you are a customer support assistant for a mobile/laptop company.
#TASK
you have to look into the issue and CLASSIFY the issue
#CONSTRAINTS
you have to classify the every issue only from the specified category of issues  into Technical, Billing, Return
#OUTPUT FORMAT
the output must be of "SINGLE WORD" only. the word must be from the category of issue given in the constraints
This is a user prompt:
I want to buy my girfriend
"""
# print(llm_res(prompt_with_output_format))
# Billing

prompt_with_example = """
#ROLE
you are a customer support assistant for a mobile/laptop company.
#TASK
you have to look into the issue and CLASSIFY the issue
#CONSTRAINTS
you have to classify the every issue only from the specified category of issues  into Technical, Billing, Return
#OUTPUT FORMAT
the output must be of "SINGLE WORD" only. the word must be from the category of issue given in the constraints
#Example
for instance if the user says he wants a refund then categories that issue as "return"
This is a user prompt:
I want to give my mobile
"""
# print(llm_res(prompt_with_example))  #Return

good_prompt = """
#ROLE
you are a customer support assistant for a mobile/laptop company.
#TASK
you have to look into the issue and CLASSIFY the issue
#CONSTRAINTS
you have to classify the every issue only from the specified category of issues  into Technical, Billing, Return
#OUTPUT FORMAT
the output must be of "SINGLE WORD" only. the word must be from the category of issue given in the constraints
#Example
for instance if the user says he wants a refund then categories that issue as "return"
#FALLBACK
if the issue is completely unrelated then categories that issue as "OTHER"
This is a user prompt:
I want my laptop back
"""
print(llm_res(good_prompt))