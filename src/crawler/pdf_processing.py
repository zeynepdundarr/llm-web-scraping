import requests
import fitz
from src.export.data_to_excel import append_pdf_to_excel

def filter_pdf_links(company_name, website, links):
    keywords = ["finance", "financial", "financialreport"]
    filtered_pdf_links = []

    for link in links:
        if link.strip().lower().endswith('.pdf'):
            url_contains_keyword = False
            content_contains_keyword = False
            
            for keyword in keywords:
                if keyword in link.strip().lower():
                    print("PDF is found with keywords")
                    url_contains_keyword = True
                    break 

            if not url_contains_keyword:
                for keyword in keywords:
                    if pdf_word_scanner(link, keyword):
                        content_contains_keyword = True
                        break

            if url_contains_keyword or content_contains_keyword:
                filtered_pdf_links.append(link)
                try:
                    response = requests.get(link)
                    with open(f'/home/zeynep/Projects/side-projects/llm-project/downloads/{link.split("/")[-1]}', 'wb') as f:
                        f.write(response.content)
                    append_pdf_to_excel(company_name, website, link)
                except Exception as e:
                    print(f"Failed to download {link}: {e}")

    return filtered_pdf_links

def pdf_word_scanner(pdf_url, keyword):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        
        with fitz.open(stream=response.content, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            if keyword in text.lower():
                return True
    except Exception as e:
        print(f"Failed to scan {pdf_url}: {e}")
    return False