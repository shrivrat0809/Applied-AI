import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import json
from pydantic import BaseModel
load_dotenv()

my_api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

complaint = "hello my name is shrivrat mani tripathi, i recently bought an iphone but it had several os related issues so i broke it please help me resolve this issue.my email is sdjhfb@k.com my contact is 123"
complaint_msg = {
    "role": "user",
    "content": complaint
}
class Ticket(BaseModel) :
    name: str
    email: str
    phone: int | None
    issue: str

schema = Ticket.model_json_schema()

system_prompt = f"""
you are a Ticket management system and your job is to get relevant information from a user complaint matching this format 
{schema} in a json object
"""

system_msg = {
    "role": "system",
    "content": system_prompt
}
responce_format = {"type": "json_object"}

messages = [system_msg, complaint_msg]

responce = client.chat.completions.create(
    model = model,
    messages=messages,
    response_format=responce_format
)

res = responce.choices[0].message.content

data_file = json.loads(res)
ticket = Ticket(**data_file)
print(ticket.name)
print(ticket.email)
print(ticket.phone)
print(ticket.issue)
print(res)