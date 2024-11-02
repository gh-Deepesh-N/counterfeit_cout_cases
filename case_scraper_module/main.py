from scraper import scrape_multiple_pages
from utils import save_cases_to_csv

def main():
    num_pages_to_scrape = 50  # Change this as needed
    cases = scrape_multiple_pages(num_pages=num_pages_to_scrape)
    save_cases_to_csv(cases)

if __name__ == "__main__":
    main()
