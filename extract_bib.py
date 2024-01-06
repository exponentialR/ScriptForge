import os
from pathlib import Path

FILE_PATH = 'latex-bib.txt'

with open(FILE_PATH, 'r') as file:
    file_read = file.readlines()

pattern = r'\\bibitem{\w+}\s*(.+?)\s*["“].*?(\d{4}).*?(doi:\s*[\d\.\-/]+)?'


