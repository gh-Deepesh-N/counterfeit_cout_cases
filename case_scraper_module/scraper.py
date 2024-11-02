import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://indiankanoon.org/search/?formInput=counterfeit%20and%20fake%20products&pagenum="

def extract_full_document(link):
    """
    Extracts the case summary from a given 'View Full Document' link.
    
    Args:
        link (str): URL to the full document.
        
    Returns:
        tuple: Full text content and resolution status.
    """
    try:
        case_response = requests.get(link)
        case_soup = BeautifulSoup(case_response.content, 'html.parser')
        paragraphs = case_soup.find_all('p')
        full_text = " ".join([para.text for para in paragraphs[:10]])  # Extract the first 10 paragraphs
        
        status = determine_resolution_status(full_text)
        return full_text if full_text else "No content available.", status
    except Exception as e:
        print(f"Failed to retrieve full document from {link}: {e}")
        return "Full document unavailable.", "Status unavailable"

def determine_resolution_status(full_text):
    """
    Determines the resolution status of a case from its full document text.
    
    Args:
        full_text (str): The full document text.
        
    Returns:
        str: The resolution status (e.g., 'Resolved', 'Ongoing', 'Dismissed', or 'Unknown').
    """
    resolved_keywords = ["resolved", "settled", "judgment passed", "case closed", "injunction granted"]
    ongoing_keywords = ["ongoing", "hearing", "pending", "to be continued"]
    dismissed_keywords = ["dismissed", "rejected", "withdrawn"]

    for keyword in resolved_keywords:
        if keyword in full_text.lower():
            return "Resolved"
    for keyword in ongoing_keywords:
        if keyword in full_text.lower():
            return "Ongoing"
    for keyword in dismissed_keywords:
        if keyword in full_text.lower():
            return "Dismissed"
    return "Unknown"

def scrape_multiple_pages(num_pages=50):
    """
    Scrapes multiple pages from the website for case details.
    
    Args:
        num_pages (int): Number of pages to scrape.
        
    Returns:
        list: A list of dictionaries containing case details.
    """
    cases = []
    for page_num in range(1, num_pages + 1):
        print(f"Scraping page {page_num}...")
        url = BASE_URL + str(page_num)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for result in soup.find_all('div', class_='result'):
            title_tag = result.find('a')
            title = title_tag.text.strip()
            fragment_link = "https://indiankanoon.org" + title_tag['href']
            date = title.split('on')[-1].strip()
            headline = result.find('div', class_='headline').text.strip() if result.find('div', class_='headline') else "No headline available"
            source = result.find('span', class_='docsource').text.strip() if result.find('span', class_='docsource') else "No source available"

            full_document_tag = result.find('a', string='Full Document')
            if full_document_tag:
                full_document_link = "https://indiankanoon.org" + full_document_tag['href']
                full_summary, status = extract_full_document(full_document_link)
            else:
                full_summary = "No full document link available."
                status = "Status unavailable"

            cases.append({
                'Title': title,
                'Date': date,
                'Headline': headline,
                'Full Summary': full_summary,
                'Source': source,
                'Fragment Link': fragment_link,
                'Full Document Link': full_document_link if full_document_tag else "No full document link",
                'Resolution Status': status
            })

            time.sleep(2)
    
    return cases
