# import packages
import PyPDF2
import re


def scan_pdf_for_keywords():
    # open the pdf file
    reader = PyPDF2.PdfReader("/home/zeynep/Projects/side-projects/llm-project/sample_pdfs/sample_pdf_1.pdf.pdf")

    # get number of pages
    num_pages = len(reader.pages)

    # define key terms
    string = "financial"

    # extract text and do the search
    found = False
    for page in reader.pages:
        text = page.extract_text() 
        # print(text)
        res_search = re.search(string, text)
        print(res_search)
        found = True
    return found