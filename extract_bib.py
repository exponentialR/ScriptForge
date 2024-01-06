import os
import re
from pathlib import Path

FILE_PATH = 'latex-bib.txt'

with open(FILE_PATH, 'r') as file:
    file_read = file.read()
print(len(file_read))
pattern_title = r'\\bibitem{\w+}\s*(.+?)\s*["“](.+?)["”].*?(\d{4}).*?(doi:\s*[\d\.\-/]+)?'


matches = re.findall(pattern_title, file_read, re.DOTALL)

extracted_data = []
for match in matches:
    author_info, title, year, doi = match
    author_lastname = author_info.split(',')[0].split()[-1]
    doi = doi.replace('doi: ', '').strip() if doi else 'N/A'

    extracted_data.append({
        'author_lastname': author_lastname,
        'year': year,
        'title': title,
        'doi': doi
    })
