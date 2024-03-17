import pandas as pd
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os


def append_pdf_to_excel(company_name, pdf_url):
    # Define the Excel filename
    excel_filename = f'./data/output/company_websites.xlsx'

    # Create a DataFrame for the new row
    df = pd.DataFrame([{'Name': company_name, 'Website': company_name, 'PDF': pdf_url}])

    # Check if the file exists. If not, create it with column headers
    if not os.path.exists(excel_filename):
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
    else:
        # If the file exists, append data without the header
        book = load_workbook(excel_filename)
        writer = pd.ExcelWriter(excel_filename, engine='openpyxl')
        writer.book = book
        writer.sheets = {ws.title: ws for ws in book.worksheets}
        startrow = writer.sheets['Sheet1'].max_row
        
        # Convert DataFrame to rows, and skip the header row (row[0])
        rows = dataframe_to_rows(df, index=False, header=False)
        for r_idx, row in enumerate(rows, startrow + 1):  # Start writing from the next empty row
            for c_idx, value in enumerate(row, 1):  # `enumerate` is 0-based; Excel columns are 1-based
                writer.sheets['Sheet1'].cell(row=r_idx, column=c_idx, value=value)

        writer.save()

# def write_filtered_pdfs_to_file(company_website_pdfs, type):
#     data_for_df = []
#     for (name, website), pdfs in company_website_pdfs.items():
#         for pdf in pdfs:
#             data_for_df.append({'Name': name, 'Website': website, 'PDF': pdf})

#     df = pd.DataFrame(data_for_df)

#     excel_filename = f'./data/output/company_websites_{type}-expanded.xlsx'
#     df.to_excel(excel_filename, index=False)

