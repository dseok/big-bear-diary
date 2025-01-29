#!/bin/env python

# utils for running symptom scan

import google.generativeai as genai
import json
import typing_extensions as typing

# Define the JSON schema for each symptom check
class SymptomResponse(typing.TypedDict):
    symptom: str
    is_present: bool
    relevant_tokens: str

def extract_symptoms(model: genai.GenerativeModel, 
                     text: str, 
                     symptoms: list):
    # Loop over each symptom and ask Gemini whether it's present
    results = []
    for symptom in symptoms:
        print('Looking for: ' + symptom + '...')
        prompt = f"""Check the following diary entry for the presence of the 
                     symptom '{symptom}':\n\n{text}\n\nIs the symptom present? 
                     Answer 'yes' or 'no'.
                     Also, please provide the exact tokens that led you to 
                     believe that the symptom was present in the field 
                     "relevant_tokens". Separate non-consecutive
                     tokens that are relevant to the symptom with a pipe symbol
                     (|). Return an empty string if the symptom is not present
                     """
        
        # Make the API request for each symptom
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=SymptomResponse
            ),
        )
        # Access the content from the first candidate (assuming only one 
        # candidate is returned)
        candidate = response.candidates[0]  # Get the first candidate response
        
        # Extract and parse the JSON string from the content
        json_string = candidate.content.parts[0].text.strip()
        
        # Parse the JSON string into a Python dictionary
        try:
            parsed_response = json.loads(json_string)
            
            # Extract the values
            relevant_tokens = parsed_response.get("relevant_tokens")
            is_present = parsed_response.get("is_present", False)
            symptom = parsed_response.get("symptom", "")
            
            # Append the result to the list
            results.append({
                'symptom': symptom,
                'is_present': is_present,
                'relevant_tokens': relevant_tokens
            })
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for symptom '{symptom}': {e}")
            results.append({
                'symptom': symptom,
                'is_present': False,  # Default to False if there is an error
                'relevant_tokens': ""
            })
    
    return results
