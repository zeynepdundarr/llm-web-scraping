import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import concurrent.futures
import wget
from src.data_extraction.pdf_word_scanner import scan_pdf_for_keywords 

def get_all_links_with_timeout(url, timeout=5):
    """Attempt to get all links within a specified timeout."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(get_all_links, url)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            print(f"Timeout occurred while trying to get links from {url}")
            return []
        except Exception as e:
            print(f"Error occurred: {e}")
            return []
        
def get_all_links(url):
    # write causes that causes scraping to freeze
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
    keywords = ["finance", "financial", "financialreport"]
    filtered_pdf_links = []
    for link in links:
        if link.strip().lower().endswith('.pdf'):
            for keyword in keywords:
                if any(keyword in link.strip().lower()) or pdf_word_scanner(keyword):
                    filtered_pdf_links.append(link)
                    try:
                        wget.download(link, '/home/zeynep/Projects/side-projects/llm-project/downloads')
                    except Exception as e:
                        print(f"Failed to download {link}: {e}")
            
                            
    return filtered_pdf_links

def crawl_for_pdfs(url, depth, visited=None, attempts=3):
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
        # If all attempts fail and the loop is completed without entering break statement
        print("Timeout - skipping this url: ", url)
        return list(set(pdf_links))
    
    pdf_links.extend(filter_pdf_links(links))
    
    for link in links:
        if link not in visited:
            pdf_links.extend(crawl_for_pdfs(link, depth - 1, visited))
    
    return list(set(pdf_links))

def write_pdfs_to_file(website, pdfs):
    filename = f"normal_pdf_links_{website.replace('http://', '').replace('https://', '').split('/')[0]}.txt"
    with open(filename, 'w') as file:
        for pdf in pdfs:
            print(pdf)  # Print each PDF link
            file.write(pdf + '\n')
    print(f"PDF links for {website} have been written to {filename}")
    

if __name__ == "__main__":
    
    start_time = time.time()  # Start timing
    start_url = "https://www.pekao.com.pl/"

    pdfs = crawl_for_pdfs(start_url, depth=2)

    write_pdfs_to_file(start_url, pdfs)

    end_time = time.time()  # End timing
    execution_time = end_time - start_time
    print(f"Normal - Execution time: {execution_time} seconds")
 