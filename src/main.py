from company_name_extractor import extract_company_names_from_excel
from extract_pdf_links import crawl_for_pdfs
from get_company_websites import find_company_website
from pdf_processing.process_pdfs import analyze_url_for_financial_content

def main():
    company_names = extract_company_names_from_excel("/home/zeynep/side-projects/llm-project/data/ai_automation_project.xlsx")
    process_company_pdfs(company_names)

def process_company_pdfs(company_names):
    # Dictionary to store company websites as keys and list of PDF URLs as values
    company_pdfs = {}

    # Find and store websites
    for name in company_names:
        website = find_company_website(name)
        print(f"{name}: {website}")
        if website != "Website not found.":
            # Crawl for PDFs and store them directly in the dictionary
            pdfs = crawl_for_pdfs(website, depth=1)
            if pdfs:  # Check if any PDFs were found
                company_pdfs[website] = pdfs

    # Iterate over each company website and process its PDFs
    
    # TODO: mock 
    company_pdfs = {}           
    company_pdfs["a.com"] = ['a.pdf, financial.pdf']
    company_pdfs["b.com"] = ['b.pdf, financial_report.pdf' ]
    # TODO
    
    result = {} 
    for website, pdfs in company_pdfs.items():
        result[website] = []
        for pdf_url in pdfs:
            result[website].append(analyze_url_for_financial_content(pdf_url))

    print(result.items)

if __name__ == "__main__":
    main()
