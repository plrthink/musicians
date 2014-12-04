import os
import time
import pickle

import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
from bs4 import BeautifulSoup
from retrying import retry

from config import firebase, MUSICIAN_STORE, MUSICIANS_PAGE_PICKLE_PATH


BASE_PAGE_NAME = 'List of music students by teacher'

musician_page_1 = wikipedia.page("%s: A to M" % BASE_PAGE_NAME)
musician_page_2 = wikipedia.page("%s: N to Z" % BASE_PAGE_NAME)

musician_pages_map = {}

if os.path.exists(MUSICIANS_PAGE_PICKLE_PATH):
    with open(MUSICIANS_PAGE_PICKLE_PATH) as f:
        musician_pages_map = pickle.load(f)


@retry(stop_max_attempt_number=10)
def get_musician_page_by_name(name):
    page = musician_pages_map.get(name)
    if page:
        return page
    else:
        print "getting wikipage %s" % name
        try:
            wikipedia.page(name)
        except PageError:
            print "page not exist %s" % name
        except DisambiguationError:
            print "page disambiguationerror %s" % name
        return None


def get_musician_id_by_name(name):
    page = get_musician_page_by_name(name)
    return page.pageid if page else None


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


def get_all_teach_relations():
    rs = [
        get_teach_relation_by_page(page)
        for page in [musician_page_1, musician_page_2]
    ]

    relations = rs[0]

    for r in rs[1:]:
        relations.update(r)
    return relations


def get_teach_relation_by_page(page):
    relations = {}
    soup = BeautifulSoup(page.html())
    # get all h3, which is a teahcer section
    h3s = soup.findAll('h3')

    for h3 in h3s:
        # get the teacher's name
        teacher_name = h3.select('.mw-headline a')[0].attrs['title']

        # get all student's link
        atags = h3.findNext('div').select('ul li a[title]')
        student_names = map(lambda x: x.attrs['title'], atags)

        relations[teacher_name] = student_names
    return relations


def parse_person_data_info_from_table(table):
    if not table:
        return {}

    NAME_FIELD = u'Name'
    ALTERNATIVE_NAME_FIELD = u'Alternative names'
    SHORT_DESCRIPTION_FIELD = u'Short description'
    DATE_OF_BIRTH_FIELD = u'Date of birth'
    PLACE_OF_BIRTH_FIELD = u'Place of birth'
    DATE_OF_DEATH_FIELD = u'Date of death'
    PLACE_OF_DEATH_FIELD = u'Place of death'

    info = {}
    for tr in table.findAll('tr')[1:]: # skip table header th
        label_td, value_td = tr.findAll('td')
        label = label_td.text.strip()
        value = value_td.text.strip()
        info[label] = value

    return {
        'name': info.get(NAME_FIELD),
        'alternative_names': info.get(ALTERNATIVE_NAME_FIELD),
        'short_description': info.get(SHORT_DESCRIPTION_FIELD),
        'date_of_birth': info.get(DATE_OF_BIRTH_FIELD),
        'place_of_birth': info.get(PLACE_OF_BIRTH_FIELD),
        'date_of_death': info.get(DATE_OF_DEATH_FIELD),
        'place_of_death': info.get(PLACE_OF_DEATH_FIELD)
    }


teach_relations = get_all_teach_relations()


def get_students_by_name(name):
    return teach_relations.get(name, [])


def get_teachers_by_name(name):
    students = [k for k, vs in teach_relations.iteritems() if name in vs]
    return students

def get_student_ids_by_name(name):
    names = get_students_by_name(name)
    ids = [get_musician_id_by_name(name) for name in names]
    return filter(None, ids)

def get_teacher_ids_by_name(name):
    names = get_teachers_by_name(name)
    ids = [get_musician_id_by_name(name) for name in names]
    return filter(None, ids)


def get_musician_data_by_name(name):
    page = get_musician_page_by_name(name)
    if not page:
        return

    soup = BeautifulSoup(page.html())
    person_data_table = soup.find(id='persondata')
    person_data = parse_person_data_info_from_table(person_data_table)

    img = get_musician_img_by_page(page)

    return {
        "id": page.pageid,
        "teachers": get_teacher_ids_by_name(name),
        "students": get_student_ids_by_name(name),
        "name": name,
        "image": img,
        "person_data": person_data,
        "url": page.url
    }


def get_musician_img_by_page(page):
    for img in page.images:
        _, ext = os.path.splitext(img)
        if ext.lower() == '.jpg':
            return img


def store_all_musicians_data(sleep_time=3):
    all_musician_names = get_all_musician_names()

    for index, name in enumerate(all_musician_names):
        if index < 0:
            continue
        print "%s: getting musician data %s" % (index, name)
        data = get_musician_data_by_name(name)
        if not data:
            print "non data for %s" % name
            continue
        print "posting data to firebase"
        firebase.put(MUSICIAN_STORE, data["id"], data)
        time.sleep(sleep_time)


def fill_all_musicians_img(sleep_time=2):
    all_musician_names = get_all_musician_names()

    for index, name in enumerate(all_musician_names):
        if index < 2862:
            continue
        print "%s: getting musician img %s" % (index, name)
        page = get_musician_page_by_name(name)
        if not page:
            continue

        img = get_musician_img_by_page(page)
        print "posting data to firebase"
        firebase.put(MUSICIAN_STORE, page.pageid + '/image', img)
        time.sleep(sleep_time)


if __name__ == '__main__':
    # store_all_musicians_data()
    fill_all_musicians_img()
