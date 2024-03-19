from src.crawler.pdf_processing import filter_pdf_links
from ..extraction.pdf_link_extraction import get_all_links_with_timeout

def crawl_for_pdfs(company_name, website, url, depth, visited=None, attempts=3):
    if visited is None:
        visited = set()
    if url in visited or depth == 0:
        return []
    
    print(f"Crawling: {url}")
    visited.add(url)
    pdf_links = []
    
    if len(visited) > 50: 
        return list(set(pdf_links))
    
    for _ in range(attempts):
        links = get_all_links_with_timeout(url)
        if links:
            break
    else:
        print("Timeout - skipping this url: ", url)
        return list(set(pdf_links))
    
    pdf_links.extend(filter_pdf_links(company_name, website, links))
    
    for link in links:
        if link not in visited:
            pdf_links.extend(crawl_for_pdfs(company_name, website, link, depth - 1, visited))
    
    return list(set(pdf_links))
