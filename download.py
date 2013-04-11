import quizlet
import argparse
import os

def download_flashcard_set(setID):
    flashcardSet = quizlet.get_flashcard_set(setID)

    if (flashcardSet['http_code'] != 200):
        print("Unable to access flashcard set %s" % setID)
        return

    # Get computer friendly set name
    cardURL = flashcardSet['url'].split('/')[-2]
    setFilename = cardURL + ".quiz"
    setPath = os.path.join(quizlet.SET_DIR, setFilename)

    f = open(setPath, 'w')
    quizlet.save_flashcard_set_terms_to_file(flashcardSet, f)
    f.close()

    title = flashcardSet['title']
    print("Downloaded '%s' set to sets/%s" % (title, setFilename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("setID", type=str, 
        help="The set id of the flashcards you wish to download")
    args = parser.parse_args()

    if(args.setID.isdigit()):
        download_flashcard_set(args.setID)
    else:
        print("\nA valid flashcard set ID is required")
    
