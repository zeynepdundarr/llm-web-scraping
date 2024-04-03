from src.crawler.pdf_processing import filter_pdf_links
from ..extraction.pdf_link_extraction import get_all_links_with_timeout, get_all_links
import aiohttp
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

async def get_all_links_with_timeout(session, url):
    # Set a timeout for the request
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        if url == "https://www.pekaobiznes24.pl/do/LangSelect":
            print("Skipping problematic URL")
            return []
        else:
            links = []
        async with session.get(url, timeout=timeout) as response:
            # Only parse the page if the content type is HTML
            if 'text/html' in response.headers.get('Content-Type', ''):
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    full_link = urljoin(url, link['href'])
                    links.append(full_link)
                return links
                # content = await response.text()
                # links = await parse_links(content)
                # return links  # Return a list of links
    except Exception as e:
        print(f"Request to {url} failed: {e}")
        return []

async def parse_links(html_content):
    # Given the HTML content, return all the href links found
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return links

async def crawl_for_pdfs(company_name, website, url, depth, session, visited=None, attempts=3):
    if visited is None:
        visited = set()
    if url in visited or depth == 0:
        return []
    
    visited.add(url)
    pdf_links = []

    if len(visited) > 50: 
        return list(set(pdf_links))
    
    for _ in range(attempts):
        links = await get_all_links_with_timeout(session, url)
        if links:
            break
    else:
        print("Timeout - skipping this url: ", url)
        return list(set(pdf_links))

    pdf_links.extend(filter_pdf_links(company_name, website, links))

    for link in links:
        if link not in visited:
            pdf_links_from_recursive_call = await crawl_for_pdfs(company_name, website, link, depth - 1, session, visited)
            pdf_links.extend(pdf_links_from_recursive_call)

    return list(set(pdf_links))

    
# def crawl_for_pdfs(company_name, website, url, depth, visited=None, attempts=3):
#     if visited is None:
#         visited = set()
#     if url in visited or depth == 0:
#         return []
    
#     print(f"Crawling: {url}")
#     visited.add(url)
#     pdf_links = []
    
#     if len(visited) > 50: 
#         return list(set(pdf_links))
    
#     for _ in range(attempts):
#         links = get_all_links_with_timeout(url)
#         if links:
#             break
#     else:
#         print("Timeout - skipping this url: ", url)
#         return list(set(pdf_links))
    
#     pdf_links.extend(filter_pdf_links(company_name, website, links))
    
#     for link in links:
#         if link not in visited:
#             pdf_links.extend(crawl_for_pdfs(company_name, website, link, depth - 1, visited))
    
#     return list(set(pdf_links))
