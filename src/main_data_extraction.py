import time

from crawler.pdf_crawler import crawl_for_pdfs

if __name__ == "__main__":
    start_time = time.time()
    start_url = "https://www.segro.com/"
    depth = 2

    pdfs = crawl_for_pdfs(start_url, depth)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
