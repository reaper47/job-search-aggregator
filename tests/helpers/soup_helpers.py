from bs4 import BeautifulSoup


def brew_soup(html_file: str) -> BeautifulSoup:
    with open(html_file, encoding='utf-8') as f:
        return BeautifulSoup(f.read(), features='html.parser')
