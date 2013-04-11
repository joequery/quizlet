import quizlet
import argparse
import sys
import os
from random import shuffle

def quiz_from_file(setPath, opts):
    with open(setPath) as f:
        terms = []
        try:
            terms = quizlet.load_flashcard_set_terms_from_file(f)
        except Exception, e:
            print("Exception occured loading %s:\n%s" % (setPath, str(e)))

        if not len(terms):
            raise Exception("No terms found in set %s" % setPath)


    #############################################################
    # Helper function for displaying terms to the the quiz taker 
    #############################################################
    def display_intro(opts):
        print("=" * 50)
        print("Quizlet Quizzer!")
        if opts['shuffle']:
            shuffle(terms)
            print("Terms have been shuffled")

        if opts['hints']:
            print("Hints are set to 'always on'")

        print("\n(Enter h as your answer for help and options)")
        print("=" * 50 + "\n")

    def display_term(term, answerParts):
        print("\n(%d parts remaining) %s \n" % (len(answerParts), term['term']))

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
        print("hint: " + quizlet.hintify(answerParts[0]))

    def see_answer_part(answerParts):
        print(answerParts[0])
        print("You will have to repeat this question later!")

    ###############################
    # Begin the quiz!
    ###############################
    display_intro(opts)


    for questionNumber,term in enumerate(terms):
        answerParts = quizlet.get_answer_parts(term['definition'])
        print("Question %d/%d" % (questionNumber+1, len(terms)))

        while answerParts:
            if(opts['hints']):
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
            elif(quizlet.check_answer(userAnswer, answerParts)):
                print("Correct!")
            else:
                print("Incorrect")

    print("Finished!")

######################################################
# Begin script execution
######################################################
parser = argparse.ArgumentParser()
parser.add_argument("--shuffle", action="store_true", 
        help="shuffle the terms in random order")
parser.add_argument("--hints", action="store_true", 
        help="always display hints (useful for first learning terms)")
parser.add_argument("setPath", type=str, 
        help="path to the set you wish to study")
args = parser.parse_args()

setPath = args.setPath
opts = {
    "shuffle": args.shuffle,
    "hints": args.hints,
}

if(os.path.exists(setPath)):
    quiz_from_file(setPath, opts)
else:
    print("\nNo flashcard set exists at %s\n" % setPath)
