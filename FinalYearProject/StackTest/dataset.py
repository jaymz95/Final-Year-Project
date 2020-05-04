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

def query(ss):

  if len(ss.split()) >= 3:
    s = """python 3.5"""
    words = keyWords(ss)
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
    #print(words[0], words[1], words[2])   
      
    df = bq_assistant.query_to_pandas_safe(query1, max_gb_scanned = 50)
    #print(df.head(10))
    def cleanhtml(raw_html):
      parsingQuestions = np.array([[],[]])
      for i in range(0, len(raw_html)):
        l = [el for el in raw_html[i]]
        print("START****************************START")
        print(l)
        print("END****************************END")
        if len(l) > 1:
          mystring = l[1].replace('\n', ' ').replace('\r', '') # removing html formatting
        else:
          print("hererererereerer")
          print(l)
          mystring = l[0].replace('\n', ' ').replace('\r', '') # removing html formatting
        

        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

        mystring = re.sub(cleanr, '', mystring)

        n = np.array([l[0], BeautifulSoup(mystring, "lxml").text])

        parsingQuestions = np.append(parsingQuestions, n)
      print("\n*******************************************\n\n\n\n\n\n*******************************************************\n")
      return parsingQuestions


    result = cleanhtml(df[['accepted_answer', 'Q_Title', 'body']].to_numpy())
    match_index = (get_close_matches_indexes(ss, result, n=1, cutoff=0.0)[0])

    #seq = SequenceMatcher(a="NameError: name 'g' is not defined", b="i wanted to delete git branch locally but i get the error $ git branch -d remotes/origin/incident error: branch 'remotes/origin/incident' not found.  please help me to solve this problem")

    aaaa = df[['accepted_answer', 'body']].to_numpy()
    p = np.array([[],[]])
    p = np.append(aaaa, 'end')
  
    print ("answers\n")
    print(result)
    rr = np.where(p == int(result[match_index-1]))
    print (rr)
    
    userAnswer = p[rr[0]-1]
    print(p[rr[0]-1])
    print("Result: "+result[match_index-1])
  if len(ss.split()) < 3:
    userAnswer = np.array([[],[]])
    userAnswer = np.append(userAnswer, 'Sorry I did not understand. Could you give me more information')
  return userAnswer
