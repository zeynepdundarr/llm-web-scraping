
import fitz  # PyMuPDF
import requests

def pdf_word_scanner(pdf_url, keyword):
    try:
        # Download the PDF file into memory
        response = requests.get(pdf_url)
        response.raise_for_status()
        
        # Open the PDF from binary data
        with fitz.open(stream=response.content, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            if keyword in text.lower():
                return True
    except Exception as e:
        print(f"Failed to scan {pdf_url}: {e}")
    return False

def filter_pdf_links(links):
    keywords = ["finance", "financial", "financialreport"]
    filtered_pdf_links = []

    # Open a file to report keywords findings
    with open('keywords_report.txt', 'w') as report_file:
        for link in links:
            if link.strip().lower().endswith('.pdf'):
                url_contains_keyword = False
                content_contains_keyword = False
                keyword_found = ""
                
                # for keyword in keywords:
                #     if keyword in link.strip().lower():
                #         url_contains_keyword = True
                #         keyword_found = keyword
                #         break  # Stop checking other keywords if one is found

                if not url_contains_keyword:
                    for keyword in keywords:
                        if pdf_word_scanner(link, keyword):
                            content_contains_keyword = True
                            keyword_found = keyword
                            break  # Stop checking other keywords if one is found

                if url_contains_keyword or content_contains_keyword:
                    filtered_pdf_links.append(link)
                    try:
                        # Attempt to download the PDF
                        response = requests.get(link)
                        with open(f'/home/zeynep/Projects/side-projects/llm-project/downloads/{link.split("/")[-1]}', 'wb') as f:
                            f.write(response.content)

                        # Report the findings
                        if url_contains_keyword:
                            report_file.write(f"keyword in url ({keyword_found}): {link}\n")
                        if content_contains_keyword:
                            report_file.write(f"keyword in pdf content ({keyword_found}): {link}\n")

                    except Exception as e:
                        print(f"Failed to download {link}: {e}")

# Example usage:
links = ["https://www.segro.com/media/lgxg3xhc/segro-green-finance-framework.pdf", "https://mediacdn.acciona.com/media/wgigg3am/2021-non-financial-statement-report.pdf"]
filter_pdf_links(links)
