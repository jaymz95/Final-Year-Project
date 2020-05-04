import bq_helper, difflib
from difflib import SequenceMatcher
from FinalYearProject.StackTest.mydifflib import get_close_matches_indexes
import numpy as np
import re
from bs4 import BeautifulSoup
from bq_helper import BigQueryHelper
# https://www.kaggle.com/sohier/introduction-to-the-bq-helper-package
stackOverflow = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="stackoverflow")

# Method for getting the 3 largest works in the user input to query agains the dataset
def keyWords(question):
  wordArray = question.split()
  words = np.array([[]])
  index = 0

  for i in range(0, len(wordArray)):
    if len(words) < 3:
      words = np.append(words, wordArray[i])
      
    else:
      for j in range(0, len(words)):
        if len(wordArray[i]) > len(words[j]) and len(words[j]) < len(words[index]):
          index = j
      if len(wordArray[i]) > len(words[index]):
        np.put(words, [index], [wordArray[i]])
     
  return words

bq_assistant = BigQueryHelper("bigquery-public-data", "stackoverflow")

bq_assistant.list_tables()

# Main Method
def query(userInput):
  # Error handling to check if user input has 3 or more words
  if len(userInput.split()) >= 3:
    words = keyWords(userInput)
    # sorts words alphabetically
    words = sorted(words, key=len)  

    query1 = """SELECT
      qe.title As Q_Title,
      EXTRACT(YEAR FROM qe.creation_date) AS Year,
      qe.accepted_answer_id AS accepted_answer,
      an.body AS body

    FROM
      `bigquery-public-data.stackoverflow.posts_questions` qe
      LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` an
      ON qe.accepted_answer_id = an.id
    GROUP BY
      Year, qe.body, accepted_answer, an.body, qe.title
    HAVING
      qe.title LIKE '%"""+ words[2] +"""%' AND qe.title LIKE '%"""+ words[1] +"""%' AND accepted_answer > 1
    ORDER BY
      Year;
            """
    # Querying the dataset with query1
    df = bq_assistant.query_to_pandas_safe(query1, max_gb_scanned = 50)
    # print(df.head(10))

    # Error Handling if nothing is returned from query
    if df.empty == True:
      query1 = """SELECT
      qe.title As Q_Title,
      EXTRACT(YEAR FROM qe.creation_date) AS Year,
      qe.accepted_answer_id AS accepted_answer,
      an.body AS body

      FROM
        `bigquery-public-data.stackoverflow.posts_questions` qe
        LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` an
        ON qe.accepted_answer_id = an.id
      GROUP BY
        Year, qe.body, accepted_answer, an.body, qe.title
      HAVING
        qe.title LIKE '%"""+ words[1] +"""%' AND accepted_answer > 1
      ORDER BY
        Year;
              """
      
      df = bq_assistant.query_to_pandas_safe(query1, max_gb_scanned = 50)

    if df.empty == True:
      query1 = """SELECT
      qe.title As Q_Title,
      EXTRACT(YEAR FROM qe.creation_date) AS Year,
      qe.accepted_answer_id AS accepted_answer,
      an.body AS body

      FROM
        `bigquery-public-data.stackoverflow.posts_questions` qe
        LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` an
        ON qe.accepted_answer_id = an.id
      GROUP BY
        Year, qe.body, accepted_answer, an.body, qe.title
      HAVING
        qe.title LIKE '%"""+ words[0] +"""%' AND accepted_answer > 1
      ORDER BY
        Year;
              """
      df = bq_assistant.query_to_pandas_safe(query1, max_gb_scanned = 50)

    # Removes HTML formatting from dataset query results
    def cleanhtml(raw_html):
      parsingQuestions = np.array([[],[]])
      for i in range(0, len(raw_html)):
        l = [el for el in raw_html[i]]
        # Error handleing for 'end' string appaneded to the end if the array
        if len(l) > 1:
          mystring = l[1].replace('\n', ' ').replace('\r', '') # removing html formatting
        else:
          mystring = l[0].replace('\n', ' ').replace('\r', '') # removing html formatting
        
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

        mystring = re.sub(cleanr, '', mystring)

        n = np.array([l[0], BeautifulSoup(mystring, "lxml").text])

        parsingQuestions = np.append(parsingQuestions, n)
      return parsingQuestions

    # getting answers from results of query 
    result = np.array([[],[]])
    result = cleanhtml(df[['accepted_answer', 'Q_Title', 'body']].to_numpy())
    
    # original size of results array
    originalLength = len(result)
    # reshaping results array to get second column to 
    # only second column to get_close_matches_indexes (reshape to 2D array)
    result = np.reshape(result, (int(len(result)/2), 2))
    match_index = (get_close_matches_indexes(userInput, result[:,1], n=1, cutoff=0.0)[0])
    
    # retreining answers
    answersArray = np.array([[],[]])
    answersArray = np.append(df[['accepted_answer', 'body']].to_numpy(), 'end')

    # reshape to 1D array
    result = np.reshape(result, (originalLength))
    # Getting possition in array where the mathcing answer to the user input is
    rr = np.where(answersArray == int(result[match_index-1]))
    
    #initailising return type to list with asnwer and website url
    userAnswer = [answersArray[rr[0]-1], answersArray[rr[0]-2]]
  
  # error message for too short user input
  if len(userInput.split()) < 3:
    userAnswer = np.array([[],[]])
    userAnswer = np.append(userAnswer, 'Sorry I did not understand. Could you give me more information')
  
  return userAnswer
