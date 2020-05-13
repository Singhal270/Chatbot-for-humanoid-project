from __future__ import print_function
import re
import random
import pyttsx3
from six.moves import input
import nltk
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import random
import io
import string # to process standard python strings

f=open('C:/Users/MOHIT SINGHAL/Desktop/projects/topic for chatbot.txt','r',errors = 'ignore')
raw=f.read()
raw=raw.upper()# converts to lowercase
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

m=open('C:/Users/MOHIT SINGHAL/Desktop/projects/test.txt','r',errors = 'ignore')
raw_one=m.read()
raw_one=raw_one.upper()# converts to lowercase
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only
sent_tokens_one = nltk.sent_tokenize(raw_one)# converts to list of sentences 
word_tokens_one = nltk.word_tokenize(raw_one)



lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Generating response
def smartresponse(user_response):
    user_response=user_response.upper()
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        sent_tokens.remove(user_response)
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        sent_tokens.remove(user_response)
        return robo_response
        
def chatresponse(user_response):
    user_response=user_response.upper()
    robo_response=''
    sent_tokens_one.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens_one)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=smartresponse(user_response)
        sent_tokens_one.remove(user_response)
        return robo_response
    else:
        robo_response = robo_response+sent_tokens_one[idx+1]
        sent_tokens_one.remove(user_response)
        return robo_response
              




engine = pyttsx3.init()
# initialisation 
engine = pyttsx3.init() 

engine.setProperty('rate',130)


#import tkintter
from tkinter import *
from tkinter import messagebox
from quiz import takequiz
from voting import insertdata
from voting import vote
from tictaktoe import playgame

def askme(ask):
    answer = messagebox.askquestion("confirmation","Do you want to "+str(ask))
    return answer
        

        #Create window
root = Tk()

        #window title
root.title("Chatbot")
root.geometry("1920x1080+50+50")

label = Label(root, text="I am Chatty, please text in lowercase ",font="Times 20")
label.place(x=600,y=30)

label2 = Label(root,bd=1,relief ="solid",height=5, text="I am speaking",font="Times 12 ",fg ="green",justify = CENTER,width=160)
label2.place(x=50,y=250)
input_ = StringVar()
entry = Entry(root,width=100,font="times 18",fg="blue",textvariable = input_).place(x=120,y=500)




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
            #print(type(match))
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
        def clicked(): 
            user_input = (input_.get()).lower()
            if user_input:
                while user_input[-1] in "!.":
                    user_input = user_input[:-1]
                if self.respond(user_input) is None:
                    output=chatresponse(user_input)
                    print(output)
                else:
                    output=self.respond(user_input)

            check=0
            try:
                num = int(output)
            except (ValueError,TypeError):
                check=1
                
            if check==0:
                label2.configure(text=' ')
                sy=eval("f"+ str(output))
                sy()
            else:
                label2.configure(text=output)
                engine.say(output)
                engine.runAndWait()
            
            
        while user_input != quit:
            user_input = quit
            try:
                user_input = input_.get()

            except EOFError:
                print(user_input)
            bt = Button(root,text ="enter" ,font="Times 15 ", bg ="black",fg="white",command=clicked)
            bt.place(x=1350,y=500)
            root.mainloop()


def f1():
    label2.configure(text=" I will tell you funfacts by asking some questions")
    engine.say(" I will tell you funfacts by asking some questions")
    engine.runAndWait()
    answer = askme("answer the questions")
    if answer=="yes":
        takequiz()
       
        label2.configure(text="tanks you ")
    else:
        label2.configure(text="No problem")
        engine.say("No problem")
        engine.runAndWait()

def f2():
    label2.configure(text=" I want you to vote")
    engine.say(" I want you to vote")
    engine.runAndWait()
    answer = askme("vote")
    if answer=="yes":
        vote()
        label2.configure(text="tanks you for voting ")
    else:
        label2.configure(text="No problem if you don't want to vote")
        engine.say("No problem if you don't want to vote")
        engine.runAndWait()
        

def f3():
    label2.configure(text=" you can play tic tac toe, this game needs two player")
    engine.say(" you can play tic tac toe, this game needs two player")
    engine.runAndWait()
    answer = askme(" play tic tac toe")
    print(answer)
    if answer=="yes":
        playgame()
        label2.configure(text="I wish, you enjoyed")
    else:
        label2.configure(text="that's fine,if you don't want to play")
        engine.say("that's fine,if you don't want to play")
        engine.runAndWait()
                 
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today ?",]
    ],
    [
        r"(.*)name is mohit",
        ["Hello I know you, How are you today ?",]
    ],
    [
        r"(.*)can do",
        ["I can make jokes,play games,\n tell you some funfact",]
    ],
        [
        r"what(.*)want",
        ["2",]
    ],
            [
        r"(.*)funfact",
        ["1",]
    ],
            [
        r"(.*) play(.*)game",
        ["3",]
    ],
     [
        r"what is your name ?",
        ["My name is Chatty and I'm a chatbot ?",]
    ],
    [
        r"how are you ?",
        ["I'm doing good, How about You ?",]
    ],

    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind",]
    ],
    [
        r"i'm (.*) doing good",
        ["Nice to hear that","Alright :)",]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ], 
    [
        r"(.*) age?",
        ["I'm a computer program dude\nSeriously you are asking me this?",]
        
    ],
    [
        r"(.*) created ?",
        ["mohit created me using Python's NLTK library ","top secret ;)",]
    ],
    [
        r"(.*) you born| (.*) you made?",
        ['Indore,madhya pradesh',]
    ],
    [
        r"how is weather in (.*)?",
        ["Weather in %1 is awesome like always","Too hot man here in %1","Too cold man here in %1","Never even heard about %1"]
    ],
    [
        r"i work in (.*)?",
        ["%1 is an Amazing company, I have heard about it. But they are in huge loss these days.",]
    ],
    [
        r"(.*)raining in (.*)",
        ["No rain since last week here in %2","Damn its raining too much here in %2"]
    ],
    [
        r"how (.*) health(.*)",
        ["I'm a computer program, so I'm always healthy ",]
    ],
    [
        r"(.*) favourite (sports|game) ?",
        ["I'm a very big fan of Football",]
    ],
    [
        r"who (.*) sportsperson ?",
        ["Messy","Ronaldo","Roony"]
],
    
    [
        r"who (.*) moviestar|actor?",
        ["Brad Pitt"]
],
    
    
    [
        r"quit",
        ["BBye take care. See you soon :) ","It was nice talking to you. See you soon :)"]
],
]




def chatty():
        print("Hi, I'm Chatty and I chat alot ;)\nPlease type lowercase English language to start a conversation. Type quit to leave ") #default message at the star
        chat = Chat(pairs, reflections)
        chat.converse()
if __name__ == "__main__":
    chatty()
