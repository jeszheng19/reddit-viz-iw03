from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json

# date = '20171019'
# subreddits_of_interest = ['politics']
#
# with open(
# '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
#     allPosts = json.load(data_file)
date = '20171021'
subreddits_of_interest = 'politics'

# with open(
# '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
#     allPosts = json.load(data_file)
with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/experimental/Analysis/' + date + '_controversial_exp.json') as data_file:
    allPosts = json.load(data_file)

# POST TITLE CLASSIFICATION
# looks alright. Just store polarity score though.
# POSTS
# plot the compound score in the X axis.

# titles = []
#
# for post in allPosts:
#     for subreddit in subreddits_of_interest:
#         if post['subreddit'] == subreddit:
#             titles.append(post['title'])
#
# strongly_negative_cutoff = -0.75
# negative_cutoff = -0.3
# neutral_cutoff = 0.3
# positive_cutoff = 0.6
#
# strongly_negative_set = []
# negative_set = []
# neutral_set = []
# positive_set = []
# strongly_positive_set = []
#
# sid = SentimentIntensityAnalyzer()
# for title in titles:
#     #print(title)
#     ss = sid.polarity_scores(title)
#     score = ss['compound']
#     if score < strongly_negative_cutoff:
#         strongly_negative_set.append(title)
#     elif score < negative_cutoff:
#         negative_set.append(title)
#     elif score < neutral_cutoff:
#         neutral_set.append(title)
#     elif score < positive_cutoff:
#         positive_set.append(title)
#     else:
#         strongly_positive_set.append(title)
#     #print ss['compound']
#
# print 'Strongly Negative'
# for title in strongly_negative_set:
#     print title
# print ''
# print 'Negative'
# for title in negative_set:
#     print title
# print ''
# print 'Neutral'
# for title in neutral_set:
#     print title
# print ''
# print 'Positive'
# for title in positive_set:
#     print title
# print ''
# print 'Strongly Positive'
# for title in strongly_positive_set:
#     print title
# print ''

# POST COMMENT CLASSIFICATION


interested_posts = []

for post in allPosts:
    interested_posts.append(post)

sample_post = interested_posts[0]


print 'Top Comment Analysis for post:'
print sample_post['title']

comment_bank = []
for comment in sample_post['top_comments']:
    if comment['stickied']:
        print 'skipped comment!'
        continue
    comment_bank.append(comment['body'])

strongly_negative_cutoff = -0.75
negative_cutoff = -0.3
neutral_cutoff = 0.3
positive_cutoff = 0.6

strongly_negative_set = []
negative_set = []
neutral_set = []
positive_set = []
strongly_positive_set = []

sid = SentimentIntensityAnalyzer()
num_comments = 0
for comment in comment_bank:
    #print(title)
    ss = sid.polarity_scores(comment)
    score = ss['compound']
    if score < strongly_negative_cutoff:
        strongly_negative_set.append(comment)
    elif score < negative_cutoff:
        negative_set.append(comment)
    elif score < neutral_cutoff:
        neutral_set.append(comment)
    elif score < positive_cutoff:
        positive_set.append(comment)
    else:
        strongly_positive_set.append(comment)
    num_comments+=1
print "Number of Comments: ", num_comments

print 'Strongly Negative'
for title in strongly_negative_set:
    print title
    print ''
print ''
print 'Negative'
for title in negative_set:
    print title
    print ''
print ''
print 'Neutral'
for title in neutral_set:
    print title
    print ''
print ''
print 'Positive'
for title in positive_set:
    print title
    print ''
print ''
print 'Strongly Positive'
for title in strongly_positive_set:
    print title
    print ''
print ''

# do i want to do any preprocessing?

# COMMENTS
# use compound score to classify whether a comment is top ....
