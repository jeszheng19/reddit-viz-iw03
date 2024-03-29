from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from models import TopPost, ControversialPost
from topicmodel import get_topics
import json
import time
from rq import Queue
from rq.job import Job
from worker import conn
from module_functions import *

# -----------------------------------------------------------------------------#
# app.py
# -----------------------------------------------------------------------------#
# This is the main file for the flask application. It handles user input
# to analyze new datasets (endpoint /updateDataset), enqueues the call to
# compute the new dataset information in the worker dyno, and fetches
# the completed computation (endpoint /results/<job_key>) and passes the
# information to the front end.
# -----------------------------------------------------------------------------#

app = Flask(__name__)

# Currently used database URL.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cmodmuptjjyklg:e48f9a96060da864807bd5b967ea0447fd5c4814a7583facde3afd9d729726ce@ec2-184-72-248-8.compute-1.amazonaws.com:5432/dbogg3844cnn32'

# Previously used database URL.
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cqvjbobiquqase:a7d4d05d62c673ed79207cd44c9ae86573c164871b6c26e6b46bed410624295e@ec2-54-221-221-153.compute-1.amazonaws.com:5432/dac5ce63jaaa4s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)
db = SQLAlchemy(app)
q = Queue(connection=conn)

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        top_titles = job.result['top_titles']
        controversial_titles = job.result['controversial_titles']
        topic_model_data_day = job.result['topic_model_data_day']
        subreddit_of_interest = job.result['subreddit_of_interest']
        start_date = job.result['start_date']
        end_date = job.result['end_date']
        posneg_data = job.result['posneg_data']
        top_post_data = job.result['top_post_data']
        controversial_post_data = job.result['controversial_post_data']
        top_domains_categories = job.result['top_domains_categories']
        controversial_domains_categories = job.result['controversial_domains_categories']
        top_titles_by_day = job.result['top_titles_by_day']
        controversial_titles_by_day = job.result['controversial_titles_by_day']
        return render_template('index.html',
                                        top_titles = top_titles,
                                        controversial_titles = controversial_titles,
                                        topic_model_data_day = topic_model_data_day,
                                        sub = subreddit_of_interest,
                                        start_date = start_date,
                                        end_date = end_date,
                                        posneg_data = posneg_data,
                                        top_post_data = top_post_data,
                                        controversial_post_data = controversial_post_data,
                                        top_domains_categories = top_domains_categories,
                                        controversial_domains_categories = controversial_domains_categories,
                                        top_titles_by_day = top_titles_by_day,
                                        controversial_titles_by_day = controversial_titles_by_day
                                        )
    else:
        return "NOT COMPLETED"

@app.route('/updateDataset', methods=['POST'])
def updateDataset():
    subreddit =  request.form['subreddit']
    subreddit_of_interest = subreddit[2:]
    date_range_str = request.form['daterange']
    start_date = int(date_range_str[6:10]+date_range_str[0:2]+date_range_str[3:5])
    end_date = int(date_range_str[19:23]+date_range_str[13:15]+date_range_str[16:18])
    job = q.enqueue_call( func=dataToBeRendered, args=(subreddit_of_interest,start_date,end_date,), result_ttl=30)
    return job.get_id()

@app.route('/')
def main():
    return render_template('index.html',
                                    top_titles = ['top titles will be displayed here'],
                                    controversial_titles = ['controversial titles will be displayed here'],
                                    topic_model_data_day = [],
                                    sub = 'politics',
                                    start_date = 20171001,
                                    end_date = 20171001,
                                    posneg_data = [],
                                    top_post_data = [],
                                    controversial_post_data = [],
                                    top_domains_categories = [],
                                    controversial_domains_categories = [],
                                    top_titles_by_day = [],
                                    controversial_titles_by_day = []
                                    )

if __name__ == '__main__':
    app.debug = False # debug setting!
    app.run()
