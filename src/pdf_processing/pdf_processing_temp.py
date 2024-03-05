import os
from openai import OpenAI

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

def analyze_url_for_financial_content(url: str) -> str:
    # Adjust the prompt as needed to direct the LLM to identify financial content
    prompt = "Identify if the following text contains financial information: " + url
    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": {prompt}},
    ]
    )

    return response.choices[0].text.strip()

# Example usage
if __name__ == "__main__":
    pdf_urls = ["https://example.com/path/to/financial_report.pdf", "x.pdf"]

    results = []
    for url in pdf_urls:
        results.append(analyze_url_for_financial_content(url))
       
    print(results)

