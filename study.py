import quizlet
import argparse
import sys
import os
from random import shuffle

def quiz_from_file(setPath, hints):
    f = open(setPath)
    terms = []
    try:
        terms = quizlet.load_flashcard_set_terms_from_file(f)
    except Exception, e:
        print("Exception occured loading %s:\n%s" % (setPath, str(e)))

    if not len(terms):
        raise Exception("No terms found in set %s" % setPath)

    shuffle(terms)

    #############################################################
    # Helper function for displaying terms to the the quiz taker 
    #############################################################
    def display_intro():
        print("=" * 50)
        print("Quizlet Quizzer!")
        print("(Enter h as your answer for help and options)")
        print("=" * 50 + "\n")

    def display_term(term, answerParts):
        print("\n(%d parts remaining) %s " % (len(answerParts), term['term']))

    def display_help():
        print("\n=============================================================")
        print("Quiz help! Current options are\n") 
        print("h: This help screen")
        print("hint: Receive a hint")
        print("see: See an answer part. You will have to repeat the question")
        print("skip: Skip this question. \n")
        print("Everything else will be considered an answer to the question")
        print("=============================================================")

    def display_hint(answerParts):
        print(quizlet.hintify(answerParts[0]))

    def see_answer_part(answerParts):
        print(answerParts[0])
        print("You will have to repeat this question later!")

    ###############################
    # Begin the quiz!
    ###############################
    display_intro()
    for questionNumber,term in enumerate(terms):
        answerParts = quizlet.get_answer_parts(term['definition'])
        print("Question %d/%d" % (questionNumber+1, len(terms)))

        while answerParts:
            if(hints):
                display_hint(answerParts)
            display_term(term, answerParts)

            userAnswer = raw_input('Your answer: ')
            print("")

            ##################
            # Command options
            ##################
            if userAnswer == "h":
                display_help()
            elif userAnswer == "hint":
                display_hint(answerParts)
            elif userAnswer == "see":
                see_answer_part(answerParts)
                # Force a repeat of this question later, but don't keep
                # appending the same question if the user wants to see more
                # answer parts.
                if(terms[-1] != term):
                    terms.append(term)
            elif userAnswer == "skip":
                break

            ###########################################
            # Check for correct answer if not an option
            ###########################################
            elif(check_answer(userAnswer, answerParts)):
                print("Correct!")
            else:
                print("Incorrect")

    print("Finished!")

######################################################
# Begin script execution
######################################################
# I don't feel like dealing with argparse. Fork if you care enough :P
if(len(sys.argv) < 2):
    print("\nFlashcard set id# or path to quizlet file required\n")
    exit()

# If a file, start the quiz
# If a set Id, get card information and save json to file.
arg = sys.argv[1]   

# If --hint flag passed, always show hints
hints = len(sys.argv) > 2 and sys.argv[2] == "--hints"

if(os.path.exists(arg)):
    quiz_from_file(arg, hints)
elif(arg.isdigit()):
    download_flashcard_set(arg)
else:
    print("\nFlashcard set id# or path to quizlet file required\n")
