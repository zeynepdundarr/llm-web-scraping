

# import packages
import PyPDF2
import re

import requests

 #def pdf_word_scanner(pdf_url, keyword):



def pdf_word_scanner(pdf_url, keyword):
    # open the pdf file
    reader = PyPDF2.PdfReader(pdf_url)

    # get number of pages
    num_pages = len(reader.pages)

    # extract text and do the search
    found = False
    for page in reader.pages:
        text = page.extract_text() 
        # print(text)
        res_search = re.search(keyword, text)
        print(res_search)
        found = True
    return found


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
                
                for keyword in keywords:
                    if keyword in link.strip().lower():
                        url_contains_keyword = True
                        keyword_found = keyword
                        break  # Stop checking other keywords if one is found

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
                        with open(f'/path/to/download/folder/{link.split("/")[-1]}', 'wb') as f:
                            f.write(response.content)

                        # Report the findings
                        if url_contains_keyword:
                            report_file.write(f"keyword in url ({keyword_found}): {link}\n")
                        if content_contains_keyword:
                            report_file.write(f"keyword in pdf content ({keyword_found}): {link}\n")

                    except Exception as e:
                        print(f"Failed to download {link}: {e}")

# Example usage:
links = ["https://www.segro.com/media/lgxg3xhc/segro-green-finance-framework.pdf", "https://www.furman.edu/first/wp-content/uploads/sites/168/2020/01/16_oct2324.pdf"]
filter_pdf_links(links)
