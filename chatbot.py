# Building a ChatBot using Tensorflow


# Importing the libraries
import numpy as np
import tensorflow as tf
import re
import time


### PART 1 ###


# Importing the data
lines = open('movie_lines.tsv', encoding='utf-8', errors='ignore').read().split('\n')
conversations = open('movie_conversations.tsv', encoding='utf-8', errors='ignore').read().split('\n')

# Creating a dictionary
lines = lines[:-1]
id_to_line = {}
for line in lines:
    if line[0] == '"':
        line = line[1:]
    if line[-1] == '"':
        line = line[:-1]
    _line = line.split('\t')
    id_to_line[_line[0]] = _line[4]

# Creating a list
conversations_ids = []
for conversation in conversations:
    _conversation = conversation.split('\t')[-1][2:-2]
    conversations_ids.append(_conversation.split("' '"))

# Separate questions and answers
questions = []
answers = []
for conversation in conversations_ids:
    for i in range(len(conversation) - 1):
        questions.append(id_to_line[conversation[i]])
        answers.append(id_to_line[conversation[i+1]])

# Further cleanings
def clean_text(text: str) -> str:
    changes = (("i'm", "i am"), ("he's", "he is"), ("she's", "she is"), ("that's", "that is"),
               ("what's", "what is"), ("it's", "it is"), ("who's", "who is"), ("\'ll", " will"),
               ("\'ve", " have"), ("\'re", " are"), ("\'d", " would"), ("won't", "will not"),
               ("can't", "cannot"))
    text = text.lower()
    for change in changes:
        text = text.replace(change[0], change[1])
    text = re.sub(r"[-()\"#/@;:<>+=~|.?,]", "", text)
    return text

clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))
    
clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))
    
# Creating a dictionary with the occurences
questions_word_to_count = {}
for question in clean_questions:
    for word in question.split():
        if word in questions_word_to_count.keys():
            questions_word_to_count[word] += 1
        else:
            questions_word_to_count[word] = 1

answers_word_to_count = {}
for answer in clean_answers:
    for word in answer.split():
        if word in answers_word_to_count.keys():
            answers_word_to_count[word] += 1
        else:
            answers_word_to_count[word] = 1
    
# Deleting the rare words
threshold = 20
questions_words_to_int = {}
word_number = 0
for word, count in questions_word_to_count.items():
    if count >= threshold:
        questions_words_to_int[word] = word_number
        word_number += 1
answers_words_to_int = {}
word_number = 0
for word, count in answers_word_to_count.items():
    if count >= threshold:
        answers_words_to_int[word] = word_number
        word_number += 1
        
# Adding the last tokens to the dictionary
tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']
for token in tokens:
    questions_words_to_int[token] = len(questions_words_to_int)
    answers_words_to_int[token] = len(answers_words_to_int)

# Inversing the dictionaries

answers_ints_to_word = {value: key for key, value in answers_words_to_int.items()}
questions_ints_to_word = {value: key for key, value in questions_words_to_int.items()}
    
# Adding the EOS token 
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'
    
# Transforming words into ints
answers_to_int = []
for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word in answers_words_to_int.keys():
            ints.append(answers_words_to_int[word])
        else:
            ints.append(answers_words_to_int['<OUT>'])
    answers_to_int.append(ints)
    
questions_to_int = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word in questions_words_to_int.keys():
            ints.append(questions_words_to_int[word])
        else:
            ints.append(questions_words_to_int['<OUT>'])
    questions_to_int.append(ints)

# Sorting questions and answers by the length of questions
sorted_clean_questions = []
sorted_clean_answers = []
questions_length = {}
for i in range(len(questions_to_int)):
    questions_length[i] = len(questions_to_int[i])
sorted_questions_length = sorted(questions_length.items(), key=lambda x:x[1])



    
    
    
    
    
    
    
    
    
    
    
    
    
    
                  