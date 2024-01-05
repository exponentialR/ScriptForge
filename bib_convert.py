import re

FILE_PATH = 'latex-bib.txt'

with open(FILE_PATH, 'r') as file:
    bib_entries = file.readlines()

print(bib_entries[:3])


def convert_bib_entry(entry):
    key_match = re.search(r"\\bibitem\{(c\d+)\}", entry)
    key = key_match.group(1) if key_match else "unknown"
    # Extract author
    author_match = re.search(r"\\bibitem\{c\d+\}\s+(.+?),", entry)
    author = author_match.group(1) if author_match else ""

    # Extract title
    title_match = re.search(r"“([^“]+?)”", entry)
    title = title_match.group(1) if title_match else ""

    # Extract journal or booktitle
    journal_booktitle_match = re.search(r",\s*“[^“]+?”\s*(.+?),\s*vol\.", entry)
    journal_booktitle = journal_booktitle_match.group(1) if journal_booktitle_match else ""

    # Extract volume and number
    volume_number_match = re.search(r",\s*vol\. (\d+)(?:, no\. (\d+))?", entry)
    volume = volume_number_match.group(1) if volume_number_match else ""
    number = volume_number_match.group(2) if volume_number_match and volume_number_match.group(2) else ""

    # Extract pages and year
    pages_year_match = re.search(r",\s*pp\. ([\d-]+),\s*(\d{4})", entry)
    pages = pages_year_match.group(1) if pages_year_match else ""
    year = pages_year_match.group(2) if pages_year_match else ""

    # Extract publisher or URL
    publisher_match = re.search(r"\[Online\]\. Available: (https?://\S+)|,\s*\[(.+?)\]\.", entry)
    publisher = publisher_match.group(1) or publisher_match.group(2) if publisher_match else ""

    # Formatting the converted entry
    converted_entry = f"@article{{{key},\n"
    converted_entry += f"  title={{\"{title}\"}},\n"
    converted_entry += f"  author={{{author}}},\n"
    converted_entry += f"  journal={{{journal_booktitle}}},\n"
    converted_entry += f"  volume={{{volume}}},\n"
    converted_entry += f"  number={{{number}}},\n"
    converted_entry += f"  pages={{{pages}}},\n"
    converted_entry += f"  year={{{year}}},\n"
    converted_entry += f"  publisher={{{publisher}}}\n"
    converted_entry += "}"
    return converted_entry


converted_entries = [convert_bib_entry(entry) for entry in bib_entries if entry.strip()]

converted_entries = "\n\n".join(converted_entries)

print(converted_entries[:1000])
