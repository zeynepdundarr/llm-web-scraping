from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with the API key from the .env file
client = OpenAI(
  api_key=os.environ.get('OPENAI_API_KEY')  # Using .get for safer access
)

def find_company_websites(company_names):
    """Finds websites for a list of company names using OpenAI."""
    websites = {}  # Dictionary to store company names and their websites
    
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



