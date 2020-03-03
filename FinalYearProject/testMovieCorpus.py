import pandas as pd
import numpy as np
import tensorflow as tf
import re
import time

#checkpoint = "best_model.ckpt" 

sess = open('best_model.ckpt.data-00000-of-00001', errors='ignore').read()


def question_to_seq(question, vocab_to_int):
    '''Prepare the question for the model'''
    
    question = clean_text(question)
    return [vocab_to_int.get(word, vocab_to_int['<UNK>']) for word in question.split()]



# Load the data
lines = open('raw_data/movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
conv_lines = open('raw_data/movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')


# In[3]:

# The sentences that we will be using to train our model.
lines[:10]


# In[4]:

# The sentences' ids, which will be processed to become our input and target data.
conv_lines[:10]


# In[5]:

# Create a dictionary to map each line's id with its text
id2line = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]


# In[6]:

# Create a list of all of the conversations' lines' ids.
convs = [ ]
for line in conv_lines[:-1]:
    _line = line.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
    convs.append(_line.split(','))


# In[7]:

convs[:10]


# In[8]:

# Sort the sentences into questions (inputs) and answers (targets)
questions = []
answers = []

for conv in convs:
    for i in range(len(conv)-1):
        questions.append(id2line[conv[i]])
        answers.append(id2line[conv[i+1]])


# In[9]:

# Check if we have loaded the data correctly
limit = 0
for i in range(limit, limit+5):
    print(questions[i])
    print(answers[i])
    print()


# In[10]:

# Compare lengths of questions and answers
print(len(questions))
print(len(answers))


# In[11]:

def clean_text(text):
    '''Clean text by removing unnecessary characters and altering the format of words.'''

    text = text.lower()
    
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"it's", "it is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "that is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"n'", "ng", text)
    text = re.sub(r"'bout", "about", text)
    text = re.sub(r"'til", "until", text)
    text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
    
    return text


# In[12]:

# Clean the data
clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))
    
clean_answers = []    
for answer in answers:
    clean_answers.append(clean_text(answer))


# In[13]:

# Take a look at some of the data to ensure that it has been cleaned well.
limit = 0
for i in range(limit, limit+5):
    print(clean_questions[i])
    print(clean_answers[i])
    print()


# In[14]:

# Find the length of sentences
lengths = []
for question in clean_questions:
    lengths.append(len(question.split()))
for answer in clean_answers:
    lengths.append(len(answer.split()))

# Create a dataframe so that the values can be inspected
lengths = pd.DataFrame(lengths, columns=['counts'])


# In[15]:

lengths.describe()


# In[16]:

print(np.percentile(lengths, 80))
print(np.percentile(lengths, 85))
print(np.percentile(lengths, 90))
print(np.percentile(lengths, 95))
print(np.percentile(lengths, 99))


# In[17]:

# Remove questions and answers that are shorter than 2 words and longer than 20 words.
min_line_length = 2
max_line_length = 20

short_questions_temp = []
short_answers_temp = []

i = 0
for question in clean_questions:
    if len(question.split()) >= min_line_length and len(question.split()) <= max_line_length:
        short_questions_temp.append(question)
        short_answers_temp.append(clean_answers[i])
    i += 1

# Filter out the answers that are too short/long
short_questions = []
short_answers = []

i = 0
for answer in short_answers_temp:
    if len(answer.split()) >= min_line_length and len(answer.split()) <= max_line_length:
        short_answers.append(answer)
        short_questions.append(short_questions_temp[i])
    i += 1


vocab = {}
for question in short_questions:
    for word in question.split():
        if word not in vocab:
            vocab[word] = 1
        else:
            vocab[word] += 1
            
for answer in short_answers:
    for word in answer.split():
        if word not in vocab:
            vocab[word] = 1
        else:
            vocab[word] += 1


threshold = 10
count = 0
for k,v in vocab.items():
    if v >= threshold:
        count += 1



questions_vocab_to_int = {}

word_num = 0
for word, count in vocab.items():
    if count >= threshold:
        questions_vocab_to_int[word] = word_num
        word_num += 1
        
answers_vocab_to_int = {}

word_num = 0
for word, count in vocab.items():
    if count >= threshold:
        answers_vocab_to_int[word] = word_num
        word_num += 1



batch_size = 128
# Create your own input question
#input_question = 'How are you?'


#sess = tf.InteractiveSession()

#sess.run(tf.global_variables_initializer())

# Use a question from the data as your input
#random = np.random.choice(len(short_questions))
#input_question = short_questions[random]
input_question = "Where are the Chicken Nuggets?"

# Prepare the question
input_question = question_to_seq(input_question, questions_vocab_to_int)

# Pad the questions until it equals the max_line_length
input_question = input_question + [questions_vocab_to_int["<PAD>"]] * (max_line_length - len(input_question))
# Add empty questions so the the input_data is the correct shape
batch_shell = np.zeros((batch_size, max_line_length))
# Set the first question to be out input question
batch_shell[0] = input_question    
    
# Run the model with the input question
answer_logits = sess.run(inference_logits, {input_data: batch_shell, 
                                            keep_prob: 1.0})[0]

# Remove the padding from the Question and Answer
pad_q = questions_vocab_to_int["<PAD>"]
pad_a = answers_vocab_to_int["<PAD>"]

print('Question')
print('  Word Ids:      {}'.format([i for i in input_question if i != pad_q]))
print('  Input Words: {}'.format([questions_int_to_vocab[i] for i in input_question if i != pad_q]))

print('\nAnswer')
print('  Word Ids:      {}'.format([i for i in np.argmax(answer_logits, 1) if i != pad_a]))
print('  Response Words: {}'.format([answers_int_to_vocab[i] for i in np.argmax(answer_logits, 1) if i != pad_a]))

