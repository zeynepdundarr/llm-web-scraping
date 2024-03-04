from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
  api_key=os.environ.get('OPENAI_API_KEY')
)

def find_company_websites(company_names):
    """Finds websites for a list of company names using OpenAI."""
    websites = {} 
    
    for company_name in company_names:
        prompt = f"What is the official website for {company_name}?"
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=60,
            temperature=0.3
        )
        generated_text = response.choices[0].text.strip()
        websites[company_name] = generated_text
    
    return websites



