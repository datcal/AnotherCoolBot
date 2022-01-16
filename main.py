import praw
import os
import csv
import re
import time
from keep_alive import keep_alive

reddit = praw.Reddit(
    client_id=os.getenv('client_id'),
    client_secret=os.getenv('client_secret'),
    username=os.getenv('username'),
    password=os.getenv('password'),
    user_agent="<ReplyCommentBot1.0>"
)


def clean_string(raw_string):
    cleaned_string = raw_string.lower()
    cleaned_string = re.sub(r'[^A-Za-z0-9 ]+', '', cleaned_string)
    return cleaned_string


class FunnyRedditBot:
    def __init__(self, filename):
        self.response_list = []
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            for row in csv_reader:
                self.response_list.append({
                    'phrase': clean_string(row[0]),
                    'reply': row[1]
                })

    def make_replay(self, i, comment):
        dictionary = self.response_list[i]
        comment.reply(dictionary['reply'])
        print(comment.body)
        print(dictionary['phrase'])
        print(dictionary['reply'])
        time.sleep(60 * 60 * 3)

    def find_match(self, comment):
        for i, dictionary in enumerate(self.response_list):
            if dictionary['phrase'] in clean_string(comment.body):
                self.make_replay(i, comment)


keep_alive()
bot = FunnyRedditBot("db.csv")
subreddit = reddit.subreddit("datcal")
for comment in subreddit.stream.comments(skip_existing=True):
    bot.find_match(comment)
