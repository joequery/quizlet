Quizlet Quizzer
===============

This project uses the Quizlet API to construct a quiz that allows for certain
keywords to be specified for a reasonable way to determine correctness of an
answer. Exact-string matching is excessive and makes either writing the cards or
answering the cards too difficult.

Requirements
------------

* Python 2.7
* pip/virtualenv
* [Quizlet API Client ID](https://quizlet.com/api_dashboard/)

Installation
------------

    $ git clone git://github.com/joequery/quizlet.git
    $ cd quizlet
    $ sudo pip install -r requirements.txt

Now rename `quizlet_secret-template.py` to `quizlet_secret.py`. Paste in your
[Quizlet API Client ID](https://quizlet.com/api_dashboard/) where indicated.

Creating flashcard sets
-----------------------

Create a public flashcard set on [Quizlet](http://quizlet.com/). Suppose we
create a card with the question "What are some defining characteristics of the
Python programming language?". We would structure our answer part of the
flashcard in the following way:

    * the [automatic] [process]ing of [docstrings]
    * whitespace [indent]ation for [delimit]ing [blocks]
    * [immutable] [strings]

A `*` indicates an answer part, and every flashcard should have at least one.
The words in the brackets are substrings that a user should provide in order for
the question to be considered correct. For our example above, the following
answers for the first answer part would be considered correct:

* automatic processing of docstrings
* processing of docstrings automatically
* docstrings are automatically processed

For the second answer part:

* blocks are delimited using indentation
* you delimit blocks using whitespace indentation
* indent to delimit blocks

### What's the point?

The point of this project is that exact string matching for flashcards is an
unreasonable way for a tool to help you study. By letting the user
determine what's important in a term or answer, we can create a tool that
doesn't reject an answer just because the wrong tense of a word was used or a
particular article adjective was missing.

Quizzing yourself from the command line
---------------------------------------

### Downloading a flashcard set

After creating your set, visit your flash card set in the browser. For example,

[http://quizlet.com/20147210/computer-security-management-ch5-flash-cards/](http://quizlet.com/20147210/computer-security-management-ch5-flash-cards/)

Extract the set ID from the URL and copy it to your clipboard. In the example
above, the set ID is 20147210.

Now navigate to the location you cloned this repository.

    $ cd /path/to/quizlet

We will now download the JSON representing the flashcard set.

    $ python quizlet.py 20147210
    Downloaded 'Computer Security Management Ch5' set to
    sets/computer-security-management-ch5-flash-cards.quiz



### Beginning the quiz

Now that you have the flashcard set downloaded, start the quiz by passing the
path to the quiz file you want to study to `quizlet.py`. (Tab auto-completion is
your friend here)

    $ python quizlet.py sets/computer-security-management-ch5-flash-cards.quiz

You should now see the quiz start

    ==================================================
    Quizlet Quizzer!
    (Enter h as your answer for help and options)
    ==================================================

    Question 1/41

    (5 parts remaining) List the security job titles 
    Your answer: 

Entering in `h` as your answer brings up the help menu

    =============================================================
    Quiz help! Current options are

    h: This help screen
    hint: Receive a hint
    see: See an answer part. You will have to repeat the question
    skip: Skip this question. 

    Everything else will be considered an answer to the question
    =============================================================

    (5 parts remaining) List the security job titles
    Your answer:


Enjoy studying!
