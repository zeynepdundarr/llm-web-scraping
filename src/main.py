from data_extraction.company_name_extractor import extract_company_names_from_excel
from data_extraction.pdf_link_extractor import crawl_for_pdfs
from data_extraction.company_website_extractor import find_company_website
from export.data_to_excel import write_filtered_pdfs_to_file

def main():
    company_names = extract_company_names_from_excel("./data/input/ai_automation_project.xlsx")
    process_company_pdfs(company_names)

def process_company_pdfs(company_names):
    # # SERP API key Free version is invalid
    # # uncomment this when SERP API KEY is present
    # company_website_pdfs = {}
    # for name in company_names:
    #     website = find_company_website(name)
    #     company_website_pdfs[(name, website)] = []
    #     print(f"{name}: {website}")
    #     if website != "Website not found.":
    #         pdfs = crawl_for_pdfs(website, depth=2)
    #         if pdfs:
    #             company_website_pdfs[(name, website)] = pdfs
    
    # # mock data is presented in the same format that I obtained from the code patch above, according to the SERP API"
    # company_websites = [('swisslife', 'https://www.swisslife.com/en/home.html'), ('worldline', 'https://worldline.com/'), ('givaudan','https://www.givaudan.com/')]         
    
    company_websites = [('worldline', 'https://worldline.com/')]         

    company_website_pdfs = {}
    # # comment this out when SERP API KEY is present
    for (name, website) in company_websites:
        if website != "Website not found.":
            pdfs = crawl_for_pdfs(website, depth=2)
            if pdfs:
                company_website_pdfs[(name, website)] = pdfs
                print(f"{website}: {pdfs}")

    write_filtered_pdfs_to_file(company_website_pdfs)

if __name__ == "__main__":
    main()
