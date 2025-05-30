
# HSN Code Validation and Suggestion Agent using Python-based ADK Framework (Simulated)

from fastapi import FastAPI, Query
from typing import List
import pandas as pd
import difflib
import uvicorn

# Load the dataset (CSV converted from Excel)
df = pd.read_csv("HSN_Master_Data.csv")

app = FastAPI(title="HSN Code Validation and Suggestion Agent")

# Function: Validate HSN Code
def validate_code(hsn_code: str):
    if not hsn_code.isdigit() or len(hsn_code) not in [2, 4, 6, 8]:
        return {"valid": False, "reason": "Invalid format. Should be 2, 4, 6, or 8 digit numeric code."}

    if hsn_code in df['HSNCode'].astype(str).values:
        desc = df[df['HSNCode'].astype(str) == hsn_code]['Description'].values[0]
        return {"valid": True, "description": desc}

    return {"valid": False, "reason": "HSN code not found in the dataset."}

# Function: Suggest HSN Codes by Description
def suggest_codes(query: str):
    desc_list = df['Description'].tolist()
    matches = difflib.get_close_matches(query.lower(), [desc.lower() for desc in desc_list], n=3, cutoff=0.4)

    if not matches:
        return {"suggestions": [], "message": "No relevant HSN codes found."}

    suggestions = df[df['Description'].str.lower().isin(matches)][['HSNCode', 'Description']]
    return {"suggestions": suggestions.to_dict(orient="records")}

# API Endpoint: Validate HSN Code
@app.get("/validate")
def validate(hsn_code: str = Query(..., description="Enter the HSN code to validate.")):
    return validate_code(hsn_code)

# API Endpoint: Suggest HSN Codes
@app.get("/suggest")
def suggest(description: str = Query(..., description="Describe the goods or service.")):
    return suggest_codes(description)

# Entry Point
if __name__ == "__main__":
    uvicorn.run("hsn_agent_adk_python:app", host="127.0.0.1", port=8000, reload=True)
