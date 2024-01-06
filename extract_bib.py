import os
import re
from pathlib import Path

FILE_PATH = 'latex-bib.txt'

with open(FILE_PATH, 'r') as file:
    file_read = file.readlines()

extracted_data = []
for line in file_read:
    pattern = r'\\bibitem{\w+}\s*(.*?)[“"](.+?)[”"].*?(\d{4}).*?(doi:\s*[\d\.\-/]+)?'
    match = re.search(pattern, line, re.DOTALL)
    if match:
        author_info, title, year, doi = match.groups()
        author_lastname = 'unknown'
        if author_info:
            possible_lastnames = re.split(r'[,;]', author_info)
            if possible_lastnames:
                last_word_in_author = possible_lastnames[0].split()[-1]
                author_lastname = last_word_in_author if last_word_in_author else 'Unknown'

        doi = doi.replace('doi: ', '').strip() if doi else 'N/A'
        extracted_data.append({
            'author_lastname': author_lastname,
            'title': title,
            'year': year,
            'doi': doi
        })

print(len(extracted_data))
