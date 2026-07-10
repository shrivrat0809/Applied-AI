import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key = my_api_key)

model = "llama-3.3-70b-versatile"

messages = []

prompt1 = "Hi!"
prompt2 = "write a paragraph on AI"
prompt3 = "Write a 1000 word essay on AI"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    messages.append({
        "role":"user",
        "content": prompt
    })
    responce = client.chat.completions.create(
        model = model,
        messages=messages,
        max_tokens=200 # restricting output token to 200 only
    )
    usage = responce.usage
    clean_res = responce.choices[0].message.content
    print(f"prompt = {prompt}, input token = {usage.prompt_tokens}, output token = {usage.completion_tokens}, total tokens = {usage.total_tokens}, terminate reason = {responce.choices[0].finish_reason}")

###############################################
# max_tkens => limit on under how many token the llm responce
# responce.usage => object containing token count
# prompt_tokens => number of token given from user to llm
# completion_tokens => number of tokens llm generated
# total_tokens => prompt_tokens + completion_tokens

#                                      --> "stop" => no token restriction on generating responce
# responce.choices[0].finish_reason --|
#                                      --> "length" => the responce is restricted to certain number of token
#################################################