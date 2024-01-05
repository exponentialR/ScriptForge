import requests
from bs4 import BeautifulSoup


def generate_citation_key(author_info, year):
    author_lastname = author_info.split(',')[0].split()[-1] if author_info else 'Unknown'
    year = year if year else '0000'
    return f"{author_lastname}{year}"


def search_google_scholar(query, authors=None, year=None, doi=None, citation_key=None):
    headers = {'User-Agent': 'Mozilla/5.0'}

    if authors:
        query += f' author:{authors}'
    if year:
        query += f' year :{year}'
    if doi:
        query += f' doi:{doi}'

    url = f'https://scholar.google.com/scholar?q={query}'

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    first_result = soup.find('div', class_='gs_ri')
    if first_result:
        title = first_result.find('h3', class_='gs_rt').text
        link = first_result.find('a')['href']
        abstract = first_result.find('div', class_='gs_rs').text
        author_info = first_result.find('div', class_='gs_a').text
        parts = author_info.split('-')

        venue = parts[1].strip() if len(parts) > 1 else None
        publication_year = parts[1].split(',')[-1].strip() if len(parts) > 1 else None

        if citation_key is None:
            citation_key = generate_citation_key(author_info, publication_year)

        # Formatting the result in the required bibliographic style
        return f"@article{{{citation_key},\n  title={{\"{title}\"}},\n  author={{\"{author_info}\"}},\n  journal={{\"{venue}\"}},\n  year={{\"{publication_year}\"}},\n  link={{\"{link}\"}}\n}}"

    else:
        return "No results found"


def put_ref_text(result, filename='converted_bib.txt'):
    with open(filename, 'a') as file:
        file.write(result + "\n\n")


query = "Role of facial expressions in social interactions"
result = search_google_scholar(query, year='2009', doi='10.1098/rstb.2009.0142', citation_key='Slyklatent_c18')
put_ref_text(result)
