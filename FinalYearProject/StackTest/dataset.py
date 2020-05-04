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
  # print ("**********************wordArray******************")
  # print(wordArray)

  words = np.array([[]])
  index = 0

  for i in range(0, len(wordArray)):
    if len(words) < 3:
      words = np.append(words, wordArray[i])
      # print("i: ", i)
    else:
      for j in range(0, len(words)):
        
        if len(wordArray[i]) > len(words[j]) and len(words[j]) < len(words[index]):
          index = j

      # print("len")
      # print(len(words[j]), words[j])
      # print(len(wordArray[i]), wordArray[i])
      # print("words: ", words)
      if len(wordArray[i]) > len(words[index]):
        np.put(words, [index], [wordArray[i]])
      #break
  # ind = [0, 1, 2]

  # temp = np.array([[]])
  # temp = np.put(words)

  # print("hererererererree")
  # for i in range(0, len(words)):
  #   for j in range(0, len(words)):
  #     #if len(words[i]) < len(words[i]):

  #     if len(words[i]) < len(words[j]) and i != j:
  #       largest = j
  #       smallest = i
  #     if len(words[i]) > len(words[j]) and i != j:
  #       largest = i
  #       smallest = j

  # print(words)
  return words



bq_assistant = BigQueryHelper("bigquery-public-data", "stackoverflow")

bq_assistant.list_tables()

# print(bq_assistant.list_tables())

# print(bq_assistant.head("comments", num_rows=20))

# print(bq_assistant.table_schema("comments"))
query1 = """SELECT
  EXTRACT(YEAR FROM creation_date) AS Year,
  COUNT(*) AS Number_of_Questions,
  ROUND(100 * SUM(IF(answer_count > 0, 1, 0)) / COUNT(*), 1) AS Percent_Questions_with_Answers
FROM
  `bigquery-public-data.stackoverflow.posts_questions`
GROUP BY
  Year
HAVING
  Year > 2008 AND Year < 2016
ORDER BY
  Year;
        """

query1 = """SELECT
  body ,
  EXTRACT(YEAR FROM creation_date) AS Year

FROM
  `bigquery-public-data.stackoverflow.posts_questions`
GROUP BY
  Year, body
HAVING
  body LIKE '%dataset%' AND body LIKE '%stackoverflow%' AND Year = 2016
ORDER BY
  Year;
        """
def query(ss):
  #ss = """delete a Git branch locally"""
  s = """python 3.5"""

  #ss = input("Question? : ")
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

      # soup = BeautifulSoup(html)
      # text = soup.get_text()
      #print(n)
      parsingQuestions = np.append(parsingQuestions, n)
    print("\n***********************8********************\n\n\n\n\n\n*******************************************************\n")
    return parsingQuestions


  result = cleanhtml(df[['accepted_answer', 'Q_Title', 'body']].to_numpy())

  # print ("*******************************HERE******************************************")
  # print(result)
  # print ("*******************************HERE******************************************")

  #v = difflib.get_close_matches("NameError: name 'g' is not defined", r, n=1, cutoff=0.0)

  # indexes = (np.array([0, 1]))
  # print(result[indexes])
  # print("wgwertuiplmmooooo")

  # result = np.reshape(result, (-1, 2))
  # x_new = result[0,:]
  # #result = np.where(r[1] == v)
  # print(result)
  # print(x_new)
  # print(result[np.ix_(0,0)])
  # print(result[0][1])
  # print(result[0])
  # print(result[1])
  # print(result[2])
  # print(result[3])

  # print(difflib.get_close_matches("NameError: name 'g' is not defined", result, n=1, cutoff=0.0))
  # print(get_close_matches_indexes("NameError: name 'g' is not defined", result, n=1, cutoff=0.0))
  #yes = difflib.get_close_matches(ss, df)
  #print (df.Q_Title)

  # print(get_close_matches_indexes("NameError: name 'g' is not defined", result, n=1, cutoff=0.0)[0])
  match_index = (get_close_matches_indexes(ss, result, n=1, cutoff=0.0)[0])
  #print (result[match_index+1])
  # print (result[match_index-1])
  # print (result[match_index])

  seq = SequenceMatcher(a="NameError: name 'g' is not defined", b="i wanted to delete git branch locally but i get the error $ git branch -d remotes/origin/incident error: branch 'remotes/origin/incident' not found.  please help me to solve this problem")
  # print(seq.ratio())

  # print ("*********************************ANSWER*****************************************")

  #parsing = np.array([[],[]])

  aaaa = df[['accepted_answer', 'body']].to_numpy()
  p = np.array([[],[]])
  p = np.append(aaaa, 'end')
  #parsing = aaaa
  # print("yeahhhhh")
  print("\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\n\n\n\n\n\n\n\n\n\n\n\n")
  print(p)
  # print("yeahhhhh2\n")
  # answer = difflib.get_close_matches(result[match_index-1], aaaa, n=1, cutoff=0.0)
  # # print(answer)
  # answers = cleanhtml(aaaa)
  # print ("answers\n")
  # print(result[match_index-1])
  rr = np.where(p == int(result[match_index-1]))
  #rr = cleanhtml(rr)
  print (rr)
  # print("Stuck on get close matches????")
  #print(difflib.get_close_matches(result[match_index-1], p, n=1, cutoff=0.0))
  #m = get_close_matches_indexes(result[match_index-1], p, n=1, cutoff=0.0)[0]
  #print (get_close_matches_indexes(result[match_index+1], answers, n=1, cutoff=0.0)[0])
  # print (p[rr])
  # print (p[rr[0]-1])#answer
  userAnswer = p[rr[0]-1]
  print(p[rr[0]-1])
  print("Result: "+result[match_index-1])
  #print("aaaa: "+aaaa)
  print()
  #userAnswer = BeautifulSoup(userAnswer).get_text()
      # text = soup.get_text()
  #answers = cleanhtml(userAnswer)

  # soup = BeautifulSoup(userAnswer)
  
  # print (soup)
  # soup.get_text()
  # print (soup.get_text())
  # import markdown
  # text_to_convert = """<raw>"Hello World"</raw>"""
  # gg = markdown.markdown(userAnswer, safe_mode=False)
  # print (markdown.markdown(userAnswer, safe_mode=False))

  # cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

  # uu = re.sub(cleanr, '', userAnswer)

  # seq = SequenceMatcher(a="NameError: name 'g' is not defined", b="I want to delete a branch both locally and remotely. Failed Attempts to Delete Remote Branch $ git branch -d remotes/origin/bugfix error: branch 'remotes/origin/bugfix' not found.  $ git branch -d origin/bugfix error: branch 'origin/bugfix' not found.  $ git branch -rd origin/bugfix Deleted remote branch origin/bugfix (was 2a14ef7).  $ git push Everything up-to-date  $ git pull From github.com:gituser/gitproject * [new branch] bugfix -> origin/bugfix Already up-to-date.  What should I do differently to successfully delete the remotes/origin/bugfix branch both locally and remotely?")
  # print(seq.ratio())

  # print("\nYear\n")
  #response1 = stackOverflow.query_to_pandas_safe(query1)
  # print(df.head(10))
  #print(userAnswer)
  
  # parsingQustions = np.array([[],[]])
  #   l = [el for el in userAnswer[i]]
  #   ans = l[1].replace('\n', ' ').replace('\r', '') # removing html formatting
  #   parsingQustions = np.append(parsingQustions, ans)
  if len(ss) < 50:
    userAnswer = "Sorry I didn't understand. Could you give me more information"
  return userAnswer
