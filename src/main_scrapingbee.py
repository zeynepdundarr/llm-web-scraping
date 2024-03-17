import time
from extraction.company_name_extractor import extract_company_names_from_excel
from extraction.pdf_link_extractor import crawl_for_pdfs
from src.extraction.pdf_link_extractor_scrapingbee import crawl_for_pdfs_enhanced
from extraction.company_website_extractor import find_company_website
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
    
    # company_websites = [('worldline', 'https://worldline.com/')]         
    # 11 : 23 AM
    company_websites = [('Bank Pekao', 'https://www.pekao.com.pl/'),
     ('Latour', 'Not found'),
     ('Renault', 'https://www.group.renault.com/'),
     ('Segro', 'https://www.segro.com/'),
    ('Freenet', 'https://www.freenet-group.de/'),
    ('Acciona', 'https://www.acciona.com/'),
    ('Caixabank', 'https://www.caixabank.com/'),
    ('Hexpol', 'https://www.hexpol.com/'),
    ('Bankinter', 'https://www.bankinter.com/'),
    ('Temenos', 'https://www.temenos.com/'),
    ('BAE Systems', 'https://www.baesystems.com/'),
    ('ACS', 'https://www.grupoacs.com/'),
    ('Pandora', 'https://www.pandoragroup.com/'),
    ('Aveva', 'https://www.aveva.com/'),
    ('HomeServe', 'Not found'),
    ('CTS Eventim', 'https://www.eventim.de/'),
    ('Accor', 'https://group.accor.com/'),
    ('Wendel', 'https://www.wendelgroup.com/en'),
    ('Reply', 'https://www.reply.com/'),
    ('Barratt Developments', 'https://www.barrattdevelopments.co.uk/'),
    ('Inditex', 'https://www.inditex.com/')]
    

    company_website_pdfs = {}
    # # comment this out when SERP API KEY is present
    for (name, website) in company_websites:
        if website != "Website not found.":
            pdfs = crawl_for_pdfs_enhanced(website, depth=2)
            if pdfs:
                company_website_pdfs[(name, website)] = pdfs
                print(f"{website}: {pdfs}")

    write_filtered_pdfs_to_file(company_website_pdfs, "scrapingbee_crawl")

if __name__ == "__main__":
    start_time = time.time()  # Start timing
    main()
    end_time = time.time()  # End timing
    execution_time = end_time - start_time
    print(f"Scrapingbee 5 - Execution time: {execution_time} seconds")


