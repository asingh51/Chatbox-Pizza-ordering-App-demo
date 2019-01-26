from __future__ import print_function

import re
import random

from six.moves import input



reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
}


class Chat(object):
    def __init__(self, pairs, reflections={}):
        """
        Initialize the chatbot.  Pairs is a list of patterns and responses.  Each
        pattern is a regular expression matching the user's statement or question,
        e.g. r'I like (.*)'.  For each such pattern a list of possible responses
        is given, e.g. ['Why do you like %1', 'Did you ever dislike %1'].  Material
        which is matched by parenthesized sections of the patterns (e.g. .*) is mapped to
        the numbered positions in the responses, e.g. %1.

        :type pairs: list of tuple
        :param pairs: The patterns and responses
        :type reflections: dict
        :param reflections: A mapping between first and second person expressions
        :rtype: None
        """

        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len, reverse=True)
        return re.compile(
            r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
        )

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(
            lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower()
        )

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find('%')
        return response

    def respond(self, str):
        """
        Generate a response to the user input.

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)  # pick a random response
                resp = self._wildcards(resp, match)  # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.':
                    resp = resp[:-2] + '.'
                if resp[-2:] == '??':
                    resp = resp[:-2] + '?'
                return resp

    # Hold a conversation with a chatbot
    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.":
                    user_input = user_input[:-1]
                respo=self.respond(user_input)
                print(respo)
                f=open("response.txt", mode='a')
                f.write("\n",user_input)
                f.write("\n",respo)




pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today ?\n", ]
    ],
    [
        r"what is your name ?",
        ["My name is FoodBox and I'm a chatbot ?\n", ]
    ],
    [
        r"how are you ?",
        ["I'm doing good. How about You ?\n", ]
    ],
    [
        r"What can I order?",
        ["Choose between pizza and Macroni\n", ]
    ],
[
        r"pizza",
        ["Medium or large?\n", ]
    ],
    [
        r"sorry (.*)",
        ["Its alright\n", "Its OK, never mind\n", ]
    ],
    [
        r"i'm (.*) doing good",
        ["Nice to hear that", "Alright :)\n", ]
    ],
    [
        r"hi|hey|hello",
        ["Hello, What would you like to order?", "Hey there, What would you like to order?\n", ]
    ],
    [
        r"what (.*) want ?",
        ["I want money in exchange of this service, a tip would be great too.\n", ]
    ],
    [
        r"(.*) created ?",
        ["Abhay created me using Python's NLTK library \n", "top secret ;)\n", ]
    ],
    [
        r"(.*) (location|city) ?",
        ['Arlington, Texas', ]
    ],
    [
        r"(.*)raining in (.*)",
        ["No rain since last week here in %2", "Damn its raining too much here in %2"]
    ],
    [
        r"how (.*) health(.*)",
        ["I'm a computer program, so I'm always healthy ", ]
    ],
    [
        r"Medium",
        ["ok. Whats your address?\n"]
    ],
    [
        r"Large",
        ["ok. Whats your address?\n"]
    ],
    [
        r"Macroni",
        ["ok. Whats your address?\n"]
    ],
    [
        r"quit",
        ["BBye take care. See you soon :) ", "It was nice talking to you. See you soon :)"]
    ],
]


def chatty():
    print("Hi, I'm FoodBox and I chat alot ;)")# \nPlease type lowercase English language to start a conversation. Type quit to leave ")  # default message at the start


chat = Chat(pairs, reflections)
chatty()
chat.converse()
