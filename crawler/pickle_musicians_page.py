
import pickle
import time

import wikipedia
from wikipedia import DisambiguationError

from retrying import retry

from get_musicians_data import get_all_musician_names
from config import MUSICIANS_PAGE_PICKLE_PATH


@retry(stop_max_attempt_number=5)
def get_wikipage_by_name(name):
    try:
        return wikipedia.page(name)
    except DisambiguationError:
        print "the wikipedia name %s has is disambiguation " % name
        return None


def get_all_pages():
    pages = {}
    all_musician_names = get_all_musician_names()
    for name in all_musician_names:
        if pages.get(name):
            print "%s already exist" % name
            continue
        print "getting wikipage %s" % name
        page = get_wikipage_by_name(name)
        if page:
            pages[name] = page
        time.sleep(1)

    return pages


def main():
    pages = get_all_pages()
    with open(MUSICIANS_PAGE_PICKLE_PATH, "w") as f:
        pickle.dump(pages, f)

if __name__ == '__main__':
    main()
