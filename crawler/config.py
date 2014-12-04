

from firebase import firebase

MUSICIANS_PAGE_PICKLE_PATH = 'musicians.pickle'

FIREBASE_BASE_PATH = "https://musicians.firebaseio.com/"

MUSICIAN_STORE = 'musicians'


firebase = firebase.FirebaseApplication(
    FIREBASE_BASE_PATH,
    None
)
