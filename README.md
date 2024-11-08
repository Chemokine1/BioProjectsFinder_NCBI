# BioProjectsFinder_NCBI

This script retrieves BioProject data from NCBI and ENA databases based on a search terms. Allowing scientists to filter researches based on projects data. Returns the newest matching projects first, based on keywords.
The results including Project identifier,  number of sequencing samples, total sequence data, storage size in terabytes, and save the results as a csv file.

## Dependencies
- `requests`
- `pandas`
- `beautifulsoup4`
- `python-dotenv`

### Usage
python bio_projects_search_and_details.py "<search_term>" [<num_results>]

### Exemple 
python BioProjectsFinder.py "microbiome cancer" 12

### Output 
```
Total records found in database: 778
Processing 12 records as requested.
           AccID Experiments Sequence_Data_Gb Storage_Size_Tb
0     PRJEB81154         N/A              N/A             N/A
1   PRJNA1179894         121                2             N/A
2   PRJNA1177512          21              N/A             N/A
3   PRJNA1177009         317            1,291            0.53
4   PRJNA1176874           7               71             N/A
5   PRJNA1174735         736            4,161            1.31
6   PRJNA1166428         N/A              N/A             N/A
7   PRJNA1158838         603               14             N/A
8   PRJNA1157538          66                1             N/A
9   PRJNA1154401          54              366            0.12
10  PRJNA1153928          44              132             N/A
11  PRJNA1153494           8              N/A             N/A
Results saved to User_path/BioProjectFinder_microbiome_cancer_12.csv
```
### Column Description
```
AccID: Project identifier (PRJNA*/PRJEB*)
Experiments: Number of sequencing samples (fastq files)
Sequence_Data_Gb: Total sequence data in gigabases 
Storage_Size_Tb: Storage size in terabytes
```
