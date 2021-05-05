'''
Optimize the query plan

Suppose we want to compose query in which we get for each question also the number of answers to this question for each
month. See the query below which does that in a suboptimal way and try to rewrite it to achieve a more optimal plan.
'''


import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, month

import os


spark = SparkSession.builder.appName('Optimize I').getOrCreate()

base_path = os.getcwd()

project_path = ('/').join(base_path.split('/')[0:-3]) 

answers_input_path = os.path.join(project_path, 'data/answers')

questions_input_path = os.path.join(project_path, 'data/questions')

answersDF = spark.read.option('path', answers_input_path).load()

questionsDF = spark.read.option('path', questions_input_path).load()

'''
Answers aggregation

Here we : get number of answers per question per month
'''

# spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
# change partitions to multiple of 16 since my local machine has 16 cores for the executor..upping to 320
spark.conf.set("spark.sql.shuffle.partitions", 320)
answers_month = answersDF.withColumn('month', month('creation_date'))\
    .groupBy('question_id', 'month')\
    .agg(count('*').alias('cnt'))

questionsMonth = questionsDF.select('question_id', 'title', 'creation_date')
#created questionsMonth to select less columns from questionsDF
resultDF = questionsMonth.join(answers_month, 'question_id').show()

'''
Task:

see the query plan of the previous result and rewrite the query to optimize it
'''
