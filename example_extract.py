#!/bin/env python

# example of running extract of diary

import google.generativeai as genai
from utils import extract_symptoms

# instantiate model
GOOGLE_API_KEY = ''
genai.configure(api_key=GOOGLE_API_KEY)
# read prompt
prompt_file = 'prompt.txt'
# prompt_file = 'prompt_wo_hitop.txt'
with open(prompt_file, 'r') as file:
    prompt = file.read()
model = genai.GenerativeModel("gemini-1.5-pro-latest", 
                              system_instruction=prompt)

# define symptoms to extract
symptoms = [
    "Elevated or expansive mood",
    "Increased energy",
    "Impulsivity",
    "Increased talkativeness",
    "Racing thoughts",
    "Distractibility",
    "Grandiosity",
    "Irritability",
    "Agitation",
    "Depressed mood",
    "Restlessness",
    "Panic attacks",
    "Suicidality"
]

# read diary
with open('example_diary.txt', 'r') as file:
    diary = file.read()

# parse symptoms
result = extract_symptoms(model=model, text=diary, symptoms=symptoms)
for res in result:
    print(f"""
          Symptom: {res['symptom']}, 
          Present: {res['is_present']},
          Relevant tokens: {res['relevant_tokens']}
          """)