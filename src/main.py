from company_name_extractor import extract_company_names_from_excel
from extract_pdf_links import crawl_for_pdfs
from get_company_websites import find_company_website
from pdf_processing.process_pdfs import analyze_url_for_financial_content

def main():
    company_names = extract_company_names_from_excel("/home/zeynep/side-projects/llm-project/data/ai_automation_project.xlsx")
    process_company_pdfs(company_names)

def process_company_pdfs(company_names):
    company_pdfs = {}

    # # TEST: Comment out below the code if you are testing it with mock data 
    for name in company_names:
        website = find_company_website(name)
        print(f"{name}: {website}")
        if website != "Website not found.":
            pdfs = crawl_for_pdfs(website, depth=1)
            if pdfs:
                company_pdfs[website] = pdfs
    
    # # TEST starts: mock company & pdfs key pair set to check 
    # # whether analyze_url_for_financial_content is working correct
                
    # company_pdfs = {}           
    # company_pdfs["a.com"] = ['a.pdf, financial.pdf']
    # company_pdfs["b.com"] = ['b.pdf, financial_report.pdf' ]
    # # TEST ends
    
    result = {} 
    for website, pdfs in company_pdfs.items():
        result[website] = []
        for pdf_url in pdfs:
            result[website].append(analyze_url_for_financial_content(pdf_url))
        print(f"Website {website},\npdfs containing finance related keywords: {result[website]}\n\n")

if __name__ == "__main__":
    main()
