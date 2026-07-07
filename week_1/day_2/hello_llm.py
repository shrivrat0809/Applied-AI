import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.environ.get("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("APT key error: API key not set !")

client = Groq(api_key = my_api_key)

model = "llama-3.3-70b-versatile"

role = "user"
prompt = "how can is Gukesh?"

message = {
    "role": role,
    "content": prompt
}

messages = [message]

response = client.chat.completions.create(
    model=model,
    messages=messages
)

print(response.choices[0].message.content)