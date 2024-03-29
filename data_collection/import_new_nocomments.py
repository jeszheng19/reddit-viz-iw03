from models import TopPost, ControversialPost, db
import json
import sys

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    # """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

def main():
    # file name.
    allPosts = []
    # date = "20171001"
    date = sys.argv[1]

    ################################################################################

    # Insert in top post data from specified date.

    ################################################################################
    with open(
    '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
        allPosts = json.load(data_file)

    #Load title pos/neg sentiments
    with open(
    '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/post-processing/jsonfiles/top_title_sentiment_' + date + '.json') as data_file:
        t_titlePosNegSentiments = json.load(data_file)

    # Only use posts in subs poltics, news, worldnews, technology
    selectPosts = []
    for post in allPosts:
        if post['subreddit'] == 'politics' or post['subreddit'] == 'news' or post['subreddit'] == 'worldnews' or post['subreddit'] == 'technology':
            selectPosts.append(post)

    for post in selectPosts:
        # filter out pinned or stickied posts.
        if post['stickied'] or post['over_18']:
            continue

        # Title Pos/Neg Sentiment processing.
        sentiment_compound = 0
        found = False
        for titleSentiment in t_titlePosNegSentiments:
            if titleSentiment['id'] == post['id']:
                sentiment_compound = titleSentiment['sentiment_compound']
                found = True
                break
        if not found:
            print 'Top title sentiment not found!' # should never occur

        # Comment Pos/Neg Sentiment processing.
        # NOT DONE FOR DATES BEFORE 10/1
        tc_strongly_pos = -1
        tc_pos = -1
        tc_neu = -1
        tc_neg = -1
        tc_strongly_neg = -1
        cc_strongly_pos = -1
        cc_pos = -1
        cc_neu = -1
        cc_neg = -1
        cc_strongly_neg = -1

        # Comment Political Sentiment processing for r/politics.
        # NOT DONE FOR DATES BEFORE 10/1
        tc_libertarian_avg = float(-1)
        tc_conservative_avg = float(-1)
        tc_liberal_avg = float(-1)
        cc_libertarian_avg = float(-1)
        cc_conservative_avg = float(-1)
        cc_liberal_avg = float(-1)

        topPost = TopPost(post['id'],
            date,
            post['permalink'],
            post['url'],
            html_escape(post['title']),
            html_escape(post['selftext']),
            post['author_link_karma'],
            post['subreddit'],
            post['score'],
            post['upvote_ratio'],
            post['num_comments'],
            post['libertarian'],
            post['green'],
            post['liberal'],
            post['conservative'],
            sentiment_compound,
            tc_strongly_pos,
            tc_pos,
            tc_neu,
            tc_neg,
            tc_strongly_neg,
            cc_strongly_pos,
            cc_pos,
            cc_neu,
            cc_neg,
            cc_strongly_neg,
            tc_libertarian_avg,
            tc_conservative_avg,
            tc_liberal_avg,
            cc_libertarian_avg,
            cc_conservative_avg,
            cc_liberal_avg)

        db.session.add(topPost)

    db.session.commit()
    print 'committed top posts from', date

    ################################################################################

    # Insert in controversial post data from specified date.

    ################################################################################

    with open(
    '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_controversial.json') as data_file:
        allPosts = json.load(data_file)

    # Load title pos/neg sentiments
    with open(
    '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/post-processing/jsonfiles/controversial_title_sentiment_' + date + '.json') as data_file:
        c_titlePosNegSentiments = json.load(data_file)

    selectPosts = []
    for post in allPosts:
        if post['subreddit'] == 'politics' or post['subreddit'] == 'news' or post['subreddit'] == 'worldnews' or post['subreddit'] == 'technology':
            selectPosts.append(post)

    # Only use posts in subs poltics, news, worldnews, technology

    for post in selectPosts:
        # filter out pinned or stickied posts.
        if post['stickied'] or post['over_18']:
            continue

        # Title Pos/Neg Sentiment processing.
        sentiment_compound = 0
        found = False
        for titleSentiment in c_titlePosNegSentiments:
            if titleSentiment['id'] == post['id']:
                sentiment_compound = titleSentiment['sentiment_compound']
                found = True
                break
        if not found:
            print 'Top title sentiment not found!', post['id'], '', post['title'] # should never occur

        controversialPost = ControversialPost(
            post['id'],
            date,
            post['permalink'],
            post['url'],
            html_escape(post['title']),
            html_escape(post['selftext']),
            post['author_link_karma'],
            post['subreddit'],
            post['score'],
            post['upvote_ratio'],
            post['num_comments'],
            post['libertarian'],
            post['green'],
            post['liberal'],
            post['conservative'],
            sentiment_compound)
        db.session.add(controversialPost)

    db.session.commit()
    print 'committed controversial posts from ', date

if __name__ == '__main__':
    main()
