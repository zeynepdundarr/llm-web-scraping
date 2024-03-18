import openpyxl
import pandas as pd
from openpyxl import Workbook


def append_pdf_to_excel(company_name, website, pdf_link):
    filename = "/home/zeynep/Projects/side-projects/llm-project/data/output/company_website_pdf.xlsx"
    try:
        try:
            workbook = openpyxl.load_workbook(filename)
        except FileNotFoundError:
            workbook = Workbook()

        sheet = workbook.active
        if sheet['A1'].value is None:
            sheet.append(["Company Name", "Website", "PDF Link"])

        sheet.append([company_name, website, pdf_link])

        workbook.save(filename)
    except Exception as e:
        print(f"Failed to append to Excel: {e}")