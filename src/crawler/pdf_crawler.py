from src.extraction.pdf_link_extraction import get_all_links_with_timeout
from .pdf_processing import filter_pdf_links

def crawl_for_pdfs(url, depth, visited=None, attempts=3):
    if visited is None:
        visited = set()
    if url in visited or depth == 0:
        return []
    print(f"Crawling: {url}")
    visited.add(url)
    pdf_links = []
    
    if len(visited) > 150: 
        return list(set(pdf_links))
    
    for _ in range(attempts):
        links = get_all_links_with_timeout(url)
        if links:
            break
    else:
        # If all attempts fail and the loop is completed without entering break statement
        print("Timeout - skipping this url: ", url)
        return list(set(pdf_links))
    
    pdf_links.extend(filter_pdf_links(links))
    
    for link in links:
        if link not in visited:
            pdf_links.extend(crawl_for_pdfs(link, depth - 1, visited))
    
    return list(set(pdf_links))
