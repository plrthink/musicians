

import time

import wikipedia
from bs4 import BeautifulSoup

from config import firebase, MUSICIAN_STORE


BASE_PAGE_NAME = 'List of music students by teacher'

musician_page_1 = wikipedia.page("%s: A to M" % BASE_PAGE_NAME)
musician_page_2 = wikipedia.page("%s: N to Z" % BASE_PAGE_NAME)


def get_all_musician_names():
    names = []

    for page in [musician_page_1, musician_page_2]:
        names += get_musician_names_by_page(page)

    return names


def get_musician_names_by_page(page):
    musicians = []

    soup = BeautifulSoup(page.html())
    teachers = soup.select('h3 span.mw-headline a')
    students = soup.select('div.div-col li a[href^=/]')
    all_musicians = teachers + students


    for musician in all_musicians:
        m_attrs = musician.attrs
        name = m_attrs['title']
        link = m_attrs['href']
        if link.startswith('/wiki/'):
            musicians.append(name)
        else:
            print 'not exist'
    return musicians


def get_musician_data_by_name(name):
    page = wikipedia.page(name)
    img = get_musician_img_by_page(page)

    return {
        "name": name,
        "image": img
    }


def get_musician_img_by_page(page):
    try:
        img = page.images[0]
    except IndexError:
        img = None
    return img


def store_all_musicians_data(sleep_time=2):
    all_musician_names = get_all_musician_names()

    for name in all_musician_names:
        print "getting musician data %s" % name
        data = get_musician_data_by_name(name)
        print "posting data to firebase"
        firebase.put(MUSICIAN_STORE, name, data)
        time.sleep(sleep_time)

if __name__ == '__main__':
    store_all_musicians_data()
