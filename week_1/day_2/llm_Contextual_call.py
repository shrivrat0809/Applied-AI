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
prompt = "who is virat kohli?"

message = {
    "role": role,
    "content": prompt
}

messages = [message]

response = client.chat.completions.create(
    model=model,
    messages=messages
)

ass_reply = response.choices[0].message.content # llm response

# adding this response in context for next question
messages.append({
    "role": "assistant",
    "content": ass_reply
})

# now we have privious messageand response in messages as a context

# prompting a contextual message
contextual_prompt = "what is his age?"
messages.append({
    "role": "user",
    "content": contextual_prompt
})

contextual_response = client.chat.completions.create(
    model=model,
    messages = messages
)

print(contextual_response.choices[0].message.content)