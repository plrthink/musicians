

import wikipedia
from bs4 import BeautifulSoup


BASE_PAGE_NAME = 'List of music students by teacher'

musician_page_1 = wikipedia.page("%s: A to M" % BASE_PAGE_NAME)
musician_page_2 = wikipedia.page("%s: N to Z" % BASE_PAGE_NAME)


def get_all_musicians_slug():
    slugs = []

    for page in [musician_page_1, musician_page_2]:
        slugs += get_musicians_slug_by_page(page)

    return slugs



def get_musicians_slug_by_page(page):
    musicians = []

    soup = BeautifulSoup(page.html())
    teachers = soup.select('h3 span.mw-headline a')
    students = soup.select('div.div-col li a[href^=/]')
    all_musicians = teachers + students


    for musician in all_musicians:
        m_attrs = musician.attrs
        link = m_attrs['href']
        if link.startswith('/wiki/'):
            slug = link.split('/')[-1]
            musicians.append(slug)
        else:
            print 'not exist'
    return musicians


def get_musician_data_by_name(name):
    page = wikipedia.page(name)
