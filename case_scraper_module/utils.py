import pandas as pd

def save_cases_to_csv(cases, filename='final_cases.csv'):
    """
    Saves the scraped cases to a CSV file.
    
    Args:
        cases (list): List of dictionaries containing case details.
        filename (str): Name of the output CSV file.
    """
    df = pd.DataFrame(cases)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
