import os
import re
from pathlib import Path


def extract_latex_bib(file_path):
    with open(file_path, 'r') as file:
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

            doi = doi.replace('doi: ', '').strip() if doi else None
            extracted_data.append({
                'author_lastname': author_lastname,
                'title': title,
                'year': year,
                'doi': doi
            })
    return extracted_data

# data_extract = extract_latex_bib(FILE_PATH)
# for data_ in data_extract:
#     print(data_)
