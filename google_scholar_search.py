import requests
from bs4 import BeautifulSoup

FILE_PATH = 'latex-bib.txt'
from extract_bib import extract_latex_bib


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
        return f"@article{{{citation_key},\n  title={{\"{title}\"}},\n  " \
               f"author={{\"{author_info}\"}},\n  " \
               f"journal={{\"{venue}\"}},\n  " \
               f"year={{\"{publication_year}\"}},\n  " \
               f"link={{\"{link}\"}}, \n abstract={{\"{abstract}\"}}}}"

    else:
        return "No results found"


def put_ref_text(result, filename='converted_bib.txt'):
    with open(filename, 'a') as file:
        file.write(result + "\n\n")


extracted_bib = extract_latex_bib(FILE_PATH)
for citation_key, data in enumerate(extracted_bib[:10]):
    query, year, doi, = data['title'], data['year'], data['doi']
    result = search_google_scholar(query, year=year, doi=doi, citation_key=f'Slyklatent_c{citation_key+1}')
    put_ref_text(result)
