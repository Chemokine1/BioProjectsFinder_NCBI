# BioProjectsFinder_NCBI

This script retrieves BioProject data from NCBI based on a search term, allowing users to filter research projects by data volume, useful for big data analysis.
The results, including project titles, accession numbers, and data volumes, are saved as a CSV file.

## Dependencies
- `requests`
- `pandas`
- `beautifulsoup4`
- `python-dotenv`

### Usage
python bio_projects_search_and_details.py "<search_term>" [<num_results>]

### exemple 
python BioProjectsFinder.py "metadata microbiome cancer" 3
