import streamlit as st
from gorq import Gorq
from prompts import SYSTEM_PROMPT
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"))

MODEL="llama-3.1-8b-instant"

def classify_po(po_description:str,Supplier:str="Not provided"):
  user_prompt = f"""
  PO Description: {po_description}
  Supplier: {Supplier}
  """
  response = client.chat.completions.create(
    model="MODEL",
    temperature=0,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

  )
  return response.choices[0].message.content