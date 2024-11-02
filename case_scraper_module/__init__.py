from case_module.scraper import scrape_multiple_pages
from case_module.utils import save_cases_to_csv

cases = scrape_multiple_pages(num_pages=10)
save_cases_to_csv(cases, 'output_cases.csv')
