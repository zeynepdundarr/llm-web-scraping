from company_name_extracter import extract_company_names_from_excel
from company_websites import find_company_websites
from extract_pdf_links_3 import crawl_for_pdfs


def get_websites_for_companies(company_names):
    """Wrapper function to input company names and get their websites."""
    company_names = company_names[0:1]
    # Finding websites for the input company names
    websites = find_company_websites(company_names)
    
    # Output: Printing the company names and their websites
    for name, website in websites.items():
        print(f"{name}: {website}")


# Example usage of the wrapper function
if __name__ == "__main__":
    file_path = '/home/zeynep/Downloads/AI Automation Project.xlsx'

    company_names = extract_company_names_from_excel(file_path, column='E')
    websites = get_websites_for_companies(company_names)
    if website:
    # # list all the pdfs
        for website in websites:
            pdf_file_names = crawl_for_pdfs(website, depth=10)
            for file_name in pdf_file_names:
                print(file_name)
