#!/usr/bin/env python3
import os
import sys

import helpers
from analyzer import Analyzer
from termcolor import colored
    
def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: ./tweets @username")
    positive = os.path.join(sys.path[0], "positive-words.txt")
    negative = os.path.join(sys.path[0], "negative-words.txt")
    analyzer = Analyzer(positive, negative)
    
    screenName = sys.argv[1].strip('@')
    
    tweets = helpers.get_user_timeline(screenName, 50)
    
    if tweets == None:
        sys.exit("User is private or doesn't exist")
        
    for tweet in tweets:
        score = analyzer.analyze(tweet)
        if score > 0.0:
            print(colored("{} {}".format(score, tweet), "green"))
        elif score < 0.0:
            print(colored("{} {}".format(score, tweet), "red"))
        else:
            print(colored("{} {}".format(score, tweet), "yellow"))

if __name__ == "__main__":
    main()
