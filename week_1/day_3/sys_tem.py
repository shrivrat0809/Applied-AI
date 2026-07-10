import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.environ.get("GOQ_API_KEY")

client = Groq(api_key = my_api_key)

messages = []

model = "llama-3.3-70b-versatile"
 ## defining system role by giving instruction
messages.append({
    "role":"system",
    "content": "you are my grandmother"
})

messages.append({
    "role": "user",
    "content": "how to live a good life"
})

## default temperature = 0
response = client.chat.completions.create(
    model = model,
    messages=messages,
    temperature  = 2
)

print(response.choices[0].message.content)


# response at temperatue = 0 => Tasty(safe => not creative)
# response at temperatue = 1 => Deliko(creative)
# response at temperatue = 2 => Flavro(very creative)


#######################
# system => assign post to llm i.e, you are junior dev, senior dev
# temperature => give diffrent personality to llm, dont be creative(0) or use creativity(2), range is [0,2]