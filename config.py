

from firebase import firebase

FIREBASE_BASE_PATH = "https://musicians.firebaseio.com/"

MUSICIAN_STORE = 'musicians'


firebase = firebase.FirebaseApplication(
    FIREBASE_BASE_PATH,
    None
)
