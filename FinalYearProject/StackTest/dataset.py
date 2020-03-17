import bq_helper, difflib
from difflib import SequenceMatcher
from mydifflib import get_close_matches_indexes
import numpy as np
import re
from bs4 import BeautifulSoup
from bq_helper import BigQueryHelper
# https://www.kaggle.com/sohier/introduction-to-the-bq-helper-package
stackOverflow = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="stackoverflow")


bq_assistant = BigQueryHelper("bigquery-public-data", "stackoverflow")

bq_assistant.list_tables()

print(bq_assistant.list_tables())

print(bq_assistant.head("comments", num_rows=20))

print(bq_assistant.table_schema("comments"))
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
        #
ss = """delete a Git branch locally"""
s = """python 3.5"""

#ss = input()
query1 = """SELECT
  qe.title As Q_Title,
  EXTRACT(YEAR FROM qe.creation_date) AS Year,
  qe.accepted_answer_id AS accepted_answer,
  an.body

FROM
  `bigquery-public-data.stackoverflow.posts_questions` qe
  LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` an
  ON qe.accepted_answer_id = an.id
GROUP BY
  Year, qe.body, accepted_answer, an.body, qe.title
HAVING
  qe.title LIKE '%"""+ ss +"""%' AND accepted_answer > 1
ORDER BY
  Year;
        """
        
df = bq_assistant.query_to_pandas_safe(query1, max_gb_scanned = 50)

def cleanhtml(raw_html):
  parsingQuestions = np.array([[],[]])
  for i in range(0, len(raw_html)):
    l = [el for el in raw_html[i]]
    #print(l[1])
    mystring = l[1].replace('\n', ' ').replace('\r', '') # removing html formatting

    n = np.array([l[0], BeautifulSoup(mystring, "lxml").text])
    parsingQuestions = np.append(parsingQuestions, n)
  return parsingQuestions


result = cleanhtml(df[['accepted_answer', 'Q_Title']].to_numpy())

print ("*******************************HERE******************************************")
print(result)
print ("*******************************HERE******************************************")

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
print(result[0])
print(result[1])
print(result[2])
print(result[3])

print(difflib.get_close_matches("NameError: name 'g' is not defined", result, n=1, cutoff=0.0))
print(get_close_matches_indexes("NameError: name 'g' is not defined", result, n=1, cutoff=0.0))
#yes = difflib.get_close_matches(ss, df)
#print (df.Q_Title)

print(get_close_matches_indexes("NameError: name 'g' is not defined", result, n=1, cutoff=0.0)[0])
match_index = (get_close_matches_indexes("NameError: name 'g' is not defined", result, n=1, cutoff=0.0)[0])
#print (result[match_index+1])
print (result[match_index-1])
print (result[match_index])

seq = SequenceMatcher(a="NameError: name 'g' is not defined", b="i wanted to delete git branch locally but i get the error $ git branch -d remotes/origin/incident error: branch 'remotes/origin/incident' not found.  please help me to solve this problem")
print(seq.ratio())

print ("*********************************ANSWER*****************************************")

#parsing = np.array([[],[]])

aaaa = df[['accepted_answer', 'body']].to_numpy()
p = np.array([[],[]])
p = np.append(aaaa, 'end')
#parsing = aaaa
print("yeahhhhh")
print(p)
print("yeahhhhh2\n")
# answer = difflib.get_close_matches(result[match_index-1], aaaa, n=1, cutoff=0.0)
# print(answer)
answers = cleanhtml(aaaa)
print (answers)
rr = np.where(p == int(result[match_index-1]))
print (rr[0])
print("Stuck on get close matches????")
#print(difflib.get_close_matches(result[match_index-1], p, n=1, cutoff=0.0))
#m = get_close_matches_indexes(result[match_index-1], p, n=1, cutoff=0.0)[0]
#print (get_close_matches_indexes(result[match_index+1], answers, n=1, cutoff=0.0)[0])
print (p[rr])
print (p[rr[0]-1])

# seq = SequenceMatcher(a="NameError: name 'g' is not defined", b="I want to delete a branch both locally and remotely. Failed Attempts to Delete Remote Branch $ git branch -d remotes/origin/bugfix error: branch 'remotes/origin/bugfix' not found.  $ git branch -d origin/bugfix error: branch 'origin/bugfix' not found.  $ git branch -rd origin/bugfix Deleted remote branch origin/bugfix (was 2a14ef7).  $ git push Everything up-to-date  $ git pull From github.com:gituser/gitproject * [new branch] bugfix -> origin/bugfix Already up-to-date.  What should I do differently to successfully delete the remotes/origin/bugfix branch both locally and remotely?")
# print(seq.ratio())

print("\nYear\n")
#response1 = stackOverflow.query_to_pandas_safe(query1)
print(df.head(10))

# query2 = """SELECT User_Tenure,
#        COUNT(1) AS Num_Users,
#        ROUND(AVG(reputation)) AS Avg_Reputation,
#        ROUND(AVG(num_badges)) AS Avg_Num_Badges
# FROM (
#   SELECT users.id AS user,
#          ROUND(TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), ANY_VALUE(users.creation_date), DAY)/365) AS user_tenure,
#          ANY_VALUE(users.reputation) AS reputation,
#          SUM(IF(badges.user_id IS NULL, 0, 1)) AS num_badges
#   FROM `bigquery-public-data.stackoverflow.users` users
#   LEFT JOIN `bigquery-public-data.stackoverflow.badges` badges
#   ON users.id = badges.user_id
#   GROUP BY user
# )
# GROUP BY User_Tenure
# ORDER BY User_Tenure;
#         """
# response2 = stackOverflow.query_to_pandas_safe(query2)
# print(response2.head(10))

# query3 = """SELECT badge_name AS First_Gold_Badge,
#        COUNT(1) AS Num_Users,
#        ROUND(AVG(tenure_in_days)) AS Avg_Num_Days
# FROM
# (
#   SELECT
#     badges.user_id AS user_id,
#     badges.name AS badge_name,
#     TIMESTAMP_DIFF(badges.date, users.creation_date, DAY) AS tenure_in_days,
#     ROW_NUMBER() OVER (PARTITION BY badges.user_id
#                        ORDER BY badges.date) AS row_number
#   FROM
#     `bigquery-public-data.stackoverflow.badges` badges
#   JOIN
#     `bigquery-public-data.stackoverflow.users` users
#   ON badges.user_id = users.id
#   WHERE badges.class = 1
# )
# WHERE row_number = 1
# GROUP BY First_Gold_Badge
# ORDER BY Num_Users DESC
# LIMIT 10;
#         """
# response3 = stackOverflow.query_to_pandas_safe(query3, max_gb_scanned=10)
# print(response3.head(10))

# query4 = """SELECT
#   Day_of_Week,
#   COUNT(1) AS Num_Questions,
#   SUM(answered_in_1h) AS Num_Answered_in_1H,
#   ROUND(100 * SUM(answered_in_1h) / COUNT(1),1) AS Percent_Answered_in_1H
# FROM
# (
#   SELECT
#     q.id AS question_id,
#     EXTRACT(DAYOFWEEK FROM q.creation_date) AS day_of_week,
#     MAX(IF(a.parent_id IS NOT NULL AND
#            (UNIX_SECONDS(a.creation_date)-UNIX_SECONDS(q.creation_date))/(60*60) <= 1, 1, 0)) AS answered_in_1h
#   FROM
#     `bigquery-public-data.stackoverflow.posts_questions` q
#   LEFT JOIN
#     `bigquery-public-data.stackoverflow.posts_answers` a
#   ON q.id = a.parent_id
#   WHERE EXTRACT(YEAR FROM a.creation_date) = 2016
#     AND EXTRACT(YEAR FROM q.creation_date) = 2016
#   GROUP BY question_id, day_of_week
# )
# GROUP BY
#   Day_of_Week
# ORDER BY
#   Day_of_Week;
#         """
# response4 = stackOverflow.query_to_pandas_safe(query4, max_gb_scanned=10)
# print(response4.head(10))



