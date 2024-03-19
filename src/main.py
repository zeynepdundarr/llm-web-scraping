import time
from src.extraction.company_name_extractor import extract_company_names_from_excel
from src.crawler.pdf_crawler import crawl_for_pdfs
from src.extraction.company_website_extractor import find_company_website

def main():
    company_names = extract_company_names_from_excel("./data/input/ai_automation_project.xlsx")
    process_company_pdfs(company_names)

def process_company_pdfs(company_names):

    company_websites = [('Segro', 'https://www.segro.com/')]
           
    for (name, website) in company_websites:
        if website != "Website not found.":
            crawl_for_pdfs(name, website, website, depth=2)

    # # SERP API key Free version is invalid
    # # uncomment this when SERP API KEY is present
    # company_website_pdfs = {}
    # for name in company_names:
    #     website = find_company_website(name)
    #     company_website_pdfs[(name, website)] = []
    #     if website != "Website not found.":
    #         crawl_for_pdfs(name, website, website, depth=2)
            
    
    # # mock data is presented in the same format that I obtained from the code patch above, according to the SERP API"
    # company_websites = [('Bank Pekao', 'https://www.pekao.com.pl/'),
    #  ('Latour', 'Not found'),
    #  ('Renault', 'https://www.group.renault.com/'),
    #  ('Segro', 'https://www.segro.com/'),        
    # ('Freenet', 'https://www.freenet-group.de/'),
    # ('Acciona', 'https://www.acciona.com/'),
    # ('Caixabank', 'https://www.caixabank.com/'),
    # ('Hexpol', 'https://www.hexpol.com/'),
    # ('Bankinter', 'https://www.bankinter.com/'),
    # ('Temenos', 'https://www.temenos.com/'),
    # ('BAE Systems', 'https://www.baesystems.com/'),
    # ('ACS', 'https://www.grupoacs.com/'),
    # ('', 'https://www.pandoragroup.com/'),
    # ('Aveva', 'https://www.aveva.com/'),
    # ('HomeServe', 'Not found'),
    # ('Accor', 'https://group.accor.com/'),
    # ('Wendel', 'https://www.wendelgroup.com/en'),
    # ('Reply', 'https://www.reply.com/'),
    # ('Barratt Developments', 'https://www.barrattdevelopments.co.uk/'),
    # ('Inditex', 'https://www.inditex.com/')]
   
     

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


