import os
from openai import OpenAI

client = OpenAI()

def analyze_url_for_financial_content(url: str) -> str:
    # Construct the prompt to identify financial content in the text from the URL
    prompt = f"Identify if the following text contains financial information: {url}"
    
    # Assuming the `client` is correctly initialized elsewhere with your OpenAI API key
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Make sure to use a model that exists at the time of your API call
        prompt=prompt,
        temperature=0,
        max_tokens=1024,  # Adjust based on your needs
    )

    return response.choices[0].text.strip()


# Example usage
if __name__ == "__main__":
    pdf_urls = ["https://example.com/path/to/financial_report.pdf", "x.pdf"]
    
    results = []
    for url in pdf_urls:
        results.append(analyze_url_for_financial_content(url))
       
    print(results)

