# Quizlet tests
import unittest
import json
import quizlet
import tempfile

NO_API_TESTS = True

class QuizletTests(unittest.TestCase):
    def test_get_answer_parts(self):
        singleAnswer = "MyAnswer\n"
        self.assertEqual(["MyAnswer"], quizlet.get_answer_parts(singleAnswer))

        multiAnswerStr = "* MyAnswer1\n* MyAnswer2"
        multiAnswerList = ["* MyAnswer1", "* MyAnswer2"]
        self.assertEqual(multiAnswerList, quizlet.get_answer_parts(multiAnswerStr))

    def test_get_keyterms(self):
        mystr = "* testing [MyKeyword] testing\n"
        self.assertEqual(["MyKeyword"], quizlet.get_keyterms(mystr))

        mystr = "* testing [Myword1 extra] testing\n"
        self.assertEqual(["Myword1 extra"], quizlet.get_keyterms(mystr))

        mystr = "* [testing]\n* [testing2 extra]"
        self.assertEqual(["testing", "testing2 extra"], quizlet.get_keyterms(mystr))

    def test_user_answer_index(self):
        answerParts = ["* t [keyword1] [keyword2] t", "* t [keyword3] t"]

        userAnswer = "I like to keyword1"
        self.assertEqual(-1, quizlet.user_answer_index(userAnswer, answerParts))

        userAnswer = "Sometimes you keyword1,keyword2"
        self.assertEqual(0, quizlet.user_answer_index(userAnswer, answerParts))

        userAnswer = "Other times you keyword3"
        self.assertEqual(1, quizlet.user_answer_index(userAnswer, answerParts))

        answerParts = ["* t [keyword1]"]

        userAnswer = "I like to keyword2"
        self.assertEqual(-1, quizlet.user_answer_index(userAnswer, answerParts))

        userAnswer = "I like to keyword1"
        self.assertEqual(0, quizlet.user_answer_index(userAnswer, answerParts))

    def test_check_answer(self):
        answerPartsOriginal = ["* t [keyword1] [keyword2] t", "* t [keyword3] t"]

        answerParts = answerPartsOriginal[:]
        userAnswer = "I like to keyword3"
        isCorrectAnswer = quizlet.check_answer(userAnswer, answerParts)

        self.assertTrue(isCorrectAnswer)
        self.assertEqual(answerParts, [answerPartsOriginal[0]])

        userAnswer = "I like to keyword1"
        isCorrectAnswer = quizlet.check_answer(userAnswer, answerParts)

        self.assertFalse(isCorrectAnswer)
        self.assertEqual(answerParts, [answerPartsOriginal[0]])

        userAnswer = "I like to keyword1 and keyword2"
        isCorrectAnswer = quizlet.check_answer(userAnswer, answerParts)

        self.assertTrue(isCorrectAnswer)
        self.assertEqual(answerParts, [])

    def test_hintify(self):
        answerParts = ["* t [keyword1] [key word two] t", "* t [keyword3] t"]

        answerPart = answerParts[0]
        self.assertEqual("* t [k_______] [k__ w___ t__] t", quizlet.hintify(answerPart))

        answerPart = answerParts[1]
        self.assertEqual("* t [k_______] t", quizlet.hintify(answerPart))
        

@unittest.skipIf(NO_API_TESTS, "Not testing API")
class QuizletAPITests(unittest.TestCase):
    def test_make_quizlet_request(self):
        setID = 19049486
        endpoint = "sets/%d" % setID
        cardSet = quizlet.make_quizlet_request(endpoint)
        self.assertEqual(cardSet['id'], setID)
        self.assertEqual(cardSet['creator']['username'], "JoeQuery")

    def test_get_flashcard_set(self):
        setID = 19049486
        cardSet = quizlet.get_flashcard_set(setID)
        self.assertEqual(cardSet['http_code'], 200)
        self.assertEqual(cardSet['id'], setID)
        self.assertEqual(cardSet['creator']['username'], "JoeQuery")

        setID = -1
        cardSet = quizlet.get_flashcard_set(setID)
        self.assertEqual(cardSet['http_code'], 410)

    def test_save_flashcard_set_terms_to_file(self):
        f = tempfile.TemporaryFile()
        setID = 19049486
        cardSet = quizlet.get_flashcard_set(setID)
        quizlet.save_flashcard_set_terms_to_file(cardSet, f)
        
        f.seek(0)
        termJSON = f.read()
        terms = json.loads(termJSON)
        f.close()

        self.assertEqual(637906377, terms[0]['id'])

    def test_load_flashcard_set_terms_from_file(self):
        f = tempfile.TemporaryFile()
        setID = 19049486
        cardSet = quizlet.get_flashcard_set(setID)
        quizlet.save_flashcard_set_terms_to_file(cardSet, f)
        
        f.seek(0)
        terms = quizlet.load_flashcard_set_terms_from_file(f)
        f.close()

        self.assertEqual(637906377, terms[0]['id'])

if __name__ == "__main__":
    unittest.main(verbosity=2)
