from company_name_extractor import extract_company_names_from_excel
from extract_pdf_links import crawl_for_pdfs, write_pdfs_to_file
from get_company_websites import find_company_website

def main():
    company_names = extract_company_names_from_excel("data/ai_automation_project.xlsx")

    websites = []
    for name in company_names:
        website = find_company_website(name)
        print(f"{name}: {website}")
        if website != "Website not found.":
            websites.append(website)

    for website in websites:
        # Consider adjusting the depth based on your needs
        pdfs = crawl_for_pdfs(website, depth=2)
        write_pdfs_to_file(website, pdfs)

if __name__ == "__main__":
    main()
