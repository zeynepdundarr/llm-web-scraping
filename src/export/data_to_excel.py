import pandas as pd

def write_filtered_pdfs_to_file(company_website_pdfs):
    data_for_df = []
    for (name, website), pdfs in company_website_pdfs.items():
        for pdf in pdfs:
            data_for_df.append({'Name': name, 'Website': website, 'PDF': pdf})

    df = pd.DataFrame(data_for_df)

    excel_filename = './data/output/company_websites_expanded.xlsx'
    df.to_excel(excel_filename, index=False)
