import time

import aiohttp
from src.extraction.company_name_extractor import extract_company_names_from_excel
from src.crawler.pdf_crawler import crawl_for_pdfs
from src.extraction.company_website_extractor import find_company_website
import asyncio

async def main():
    company_names = extract_company_names_from_excel("./data/input/ai_automation_project.xlsx")
    await process_company_pdfs(company_names)

async def process_company_pdfs(company_names):

    company_websites = [('Segro', 'https://www.segro.com/')]
    async with aiohttp.ClientSession() as session:
        tasks = []
        for (name, website) in company_websites:
            if website != "Website not found.":
                tasks.append(crawl_for_pdfs(name, website, website, depth=2, session=session))

        await asyncio.gather(*tasks)
     

if __name__ == "__main__":
    start_time = time.time()
    # main()
    asyncio.run(main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


