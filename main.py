from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Use the API key from the .env file
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

def find_company_website(company_name):

    prompt = f"What is the official website for {company_name}?"
    response = client.completions.create(model = "gpt-3.5-turbo-instruct", prompt=prompt)

    generated_text = response.choices[0].text
    print(generated_text)

    ##
    # response = openai.Completion.create(
    #     engine="text-davinci-003",  # Or use the latest available model
    #     prompt=f"What is the official website for {company_name}?",
    #     max_tokens=50,
    #     n=1,
    #     stop="\n",
    #     temperature=0.3
    # )
    # # Extracting the website URL from the response
    # website_url = response.choices[0].text.strip()
    return response.choices[0].text.strip()

# Example: Looking up websites for a list of companies
company_names = ["OpenAI", "Google", "Microsoft"]
for name in company_names:
    website = find_company_website(name)
    print(f"{name}: {website}")


