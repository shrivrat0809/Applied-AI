import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep
from pydantic import BaseModel
import json
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Api Key Error!")
    os._exit(0)

client = Groq(api_key=api_key)
model = "llama-3.3-70b-versatile"
JD="""
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""
RESUME="""
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

def llm_call(system_prompt, user_prompt):
    sys_msg = {
        "role": "system",
        "content": system_prompt
    }

    user_msg = {
        "role": "user",
        "content": user_prompt
    }

    messages = [sys_msg,user_msg]
    responce = client.chat.completions.create(messages=messages, model = model)
    result = responce.choices[0].message.content
    return result

def step1_parse_resume(RESUME) :
    print("step1")
    class Resume(BaseModel):
        skills: list[str] | None
    schema_json = json.dumps(Resume.model_json_schema())
    sys_msg = f"""
        You are a skilled Hiring Manager at a Tech company. 
        Extract all the skills of the give resume provided by a candidate.
        Only extract the skills mentioned in the resume do not invent any detail.
        Output Format:
        only return the extracted skills from the resume matching this format {schema_json}
    """
    user_msg = f"""
        Extract the skills from this Resume:
        {RESUME}
    """

    responce = llm_call(sys_msg, user_msg)
    return responce

def step2_parse_jd(JD) :
    print("step2")
    class Jd(BaseModel):
            skills: list[str] | None
    schema_json = json.dumps(Jd.model_json_schema())
    sys_msg = f"""
        You are a skilled Hiring Manager at a Tech company. 
        Extract the exact skills of given job description.
        Only extract the skills mentioned in the job description, do not invent any detail.
        Output Format:
        return the required skills matching the format: {schema_json} only.
    """
    user_msg = f"""
        Extract the skills from this Job Description:
        {JD}
    """
    
    responce = llm_call(sys_msg, user_msg)
    return responce

def step3_generate_score(user_skills, jd):
    print("step3")
    sys_msg = f"""
             You are a skilled Hiring Manager at a Tech company. 
             Comapre the skills mentioned in the job description with the Resume provided by the candidate
             Output Format:
             return the score of the Resume on the scale of 1 to 100 and also give a "verdict" on the Resume. 
    """
    user_msg = f"""
        Compare and match the skills
        JD:
        {jd}
        Candidate:
        {user_skills}
    """
    return llm_call(sys_msg,user_msg)

user_skill = step1_parse_resume(RESUME)
print(user_skill)
sleep(2)
jd = step2_parse_jd(JD)
print(jd)
sleep(2)
score = step3_generate_score(user_skill, jd)
print(score)