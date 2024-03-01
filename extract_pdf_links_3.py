import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_all_links(url):
    if url == "https://www.pekaobiznes24.pl/do/LangSelect":
        print("Skipping problematic URL")
        return []
    else:
        links = []
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_link = urljoin(url, link['href'])
                links.append(full_link)
        except Exception as e:
            print(f"Failed to get links from {url}: {e}")
        return links


def filter_pdf_links(links):
    return [link for link in links if link.lower().endswith('.pdf')]

def crawl_for_pdfs(url, depth, visited=None):
    if visited is None:
        visited = set()
    if url in visited or depth == 0:
        return []
    print(f"Crawling: {url}")
    visited.add(url)
    pdf_links = []
    
    links = get_all_links(url)
    pdf_links.extend(filter_pdf_links(links))
    
    for link in links:
        if link not in visited:
            pdf_links.extend(crawl_for_pdfs(link, depth - 1, visited))
    
    return list(set(pdf_links))

if __name__ == "__main__":
    # start_url = "https://www.pekao.com.pl/en/"
    start_url = "https://www.atlascopcogroup.com/"

    pdfs = crawl_for_pdfs(start_url, depth=10)
    
    # Write PDF links to a file
    with open('pdf_links.txt', 'w') as file:
        for pdf in pdfs:
            file.write(pdf + '\n')
    
    print(f"PDF links have been written to pdf_links.txt")