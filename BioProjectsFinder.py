import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys
import re
import os
from dotenv import load_dotenv
load_dotenv()

# Check if at least the search term is provided
if len(sys.argv) < 2:
    print("Error: Please provide a search term.")
    print("Usage: python bio_projects_search_and_details.py \"<search_term>\" [<num_results>]")
    sys.exit(1)

# Assign command-line arguments to variables
search_term = sys.argv[1]
num_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10  # Default to 10 results if not provided

# Define the API key
api_key = os.getenv('NCBI_API_KEY')

# URL for the esearch API
search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# Set parameters for the API request
search_params = {
    "db": "bioproject",
    "term": search_term,
    "retmax": num_results,
    "retmode": "json",
    "api_key": api_key
}

# Perform the search request
search_response = requests.get(search_url, params=search_params)
search_data = search_response.json()

# Extract IDs from the search results
ids = search_data.get('esearchresult', {}).get('idlist', [])

# Check the results
print(f"Found {len(ids)} records.")
if ids:
    print("First few IDs:", ids[:5])

# List of BioProject IDs to process
bioproject_ids = ids

# Base URL for fetching BioProject details
base_url = "https://www.ncbi.nlm.nih.gov/bioproject/"

# List to store extracted information
projects_data = []

for bioproject_id in bioproject_ids:
    url = f"{base_url}{bioproject_id}"
    response = requests.get(url)
    
    # Check if the response is successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title from the correct HTML tag (adjust this based on actual page structure)
        title_tag = soup.find('div', class_='rprt_all')
        title = title_tag.find('h1').text.strip() if title_tag else "No Title Found"
        
        # Extract other details with safety checks
        accession_tag = soup.find(string="Accession")
        accession = accession_tag.find_next("td").text.strip() if accession_tag else "N/A"
        
        sra_experiments_tag = soup.find(string="SRA Experiments")
        sra_experiments = sra_experiments_tag.find_next("td").text.strip() if sra_experiments_tag else "N/A"
        
        data_volume_gbases_tag = soup.find(string="Data volume, Gbases")
        data_volume_gbases = data_volume_gbases_tag.find_next("td").text.strip() if data_volume_gbases_tag else "N/A"
        
        data_volume_tbytes_tag = soup.find(string="Data volume, Tbytes")
        data_volume_tbytes = data_volume_tbytes_tag.find_next("td").text.strip() if data_volume_tbytes_tag else "N/A"

        # Append the extracted information to the list
        projects_data.append({
            "Title": title,
            "Accession": accession,
            "SRA Experiments": sra_experiments,
            "Data Volume (Gbases)": data_volume_gbases,
            "Data Volume (Tbytes)": data_volume_tbytes
        })
        
        # Debugging: Print the title and BioProject ID
        print(f"Processed BioProject ID: {bioproject_id}, Title: {title}")
        
    else:
        print(f"Failed to retrieve details for BioProject ID: {bioproject_id}")

df = pd.DataFrame(projects_data)

# Display the DataFrame in the console
print(df)

# Create a sanitized version of the search term for the filename
sanitized_search_term = re.sub(r'\W+', '_', search_term)

# Generate the filename based on the search term and number of rows
filename = f"BioProjectFinder_{sanitized_search_term}_{num_results}.csv"

# Create the "Results_BioProjectsFinder" folder if it doesn't exist
results_folder = "Results_BioProjectsFinder"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# Generate the full path for the CSV file
full_path = os.path.join(results_folder, filename)

# Save the DataFrame to the generated CSV file in the results folder
df.to_csv(full_path, index=False)

print(f"Results saved to {full_path}")
print(f"Results saved to {filename}")
