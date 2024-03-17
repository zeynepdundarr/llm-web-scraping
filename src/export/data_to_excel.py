import pandas as pd
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os

def append_pdf_to_excel(company_name, pdf_url):
    excel_filename = f'./data/output/company_websites.xlsx'

    df = pd.DataFrame([{'Name': company_name, 'Website': company_name, 'PDF': pdf_url}])

    if not os.path.exists(excel_filename):
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
    else:
        book = load_workbook(excel_filename)
        writer = pd.ExcelWriter(excel_filename, engine='openpyxl')
        writer.book = book
        writer.sheets = {ws.title: ws for ws in book.worksheets}
        startrow = writer.sheets['Sheet1'].max_row
        
        rows = dataframe_to_rows(df, index=False, header=False)
        for r_idx, row in enumerate(rows, startrow + 1):  # Start writing from the next empty row
            for c_idx, value in enumerate(row, 1):  # `enumerate` is 0-based; Excel columns are 1-based
                writer.sheets['Sheet1'].cell(row=r_idx, column=c_idx, value=value)

        writer.save()