# -*- coding: utf8 -*-
__author__ = 'Aaron'
from tkinterWindow import WbFrame
from mtTkinter import Tk
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Cursor
from tweepy import API
import argparse

consumer_key="K5V01oc6yakWzWHJEKKwNiogE"
consumer_secret="wLz6L6zjExxfmWPDFtktnqPUQ4GEhf9eDnx7W89O1veiFnVG10"

access_token="977129881-t9gDn2zoOOvAefmeF4Ic13YeLtxC5BO3JHn2USMT"
access_token_secret="Hugf9bmjvGbRYDWQP7AktmbzqN69F9XrczmbO5k39ooMZ"


#tweet_list = [] #stores tweets in list DEPRECIATED
white_board = None
stream_obj = None
oAuth_obj = None
max_tweets = 9

class WBListener(StreamListener):

    def on_status(self, status):

        white_board.add_tweet_to_board(status)
        return True

    def on_error(self, error):
        print(error)
        return white_board.draw_error(error)
        #return False



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-yh', '--height', help='window height, default is 900px', type=int)
    parser.add_argument('-xw', '--width', help='window width, default is 1600', type=int)
    parser.add_argument('-f', '--fullscreen', help='fullscreen mode', action='store_true')
    parser.add_argument('-d', '--devmode', help='draws dev grid on screen area', action='store_true')
    args = parser.parse_args()
    print(args)
    root = Tk()
    global white_board
    global oAuth_obj
    global stream_obj

    oAuth_obj = OAuthHandler(consumer_key, consumer_secret)
    oAuth_obj.set_access_token(access_token, access_token_secret)

    if args.height is not None and args.width is not None:
        print("Running at %dx%d resolution" %(args.width, args.height))
        if args.fullscreen:
            white_board = WbFrame(root, args.width, args.height, full=True);
        else:
            white_board = WbFrame(root, args.width, args.height, full=False);
    else:
        if args.fullscreen:
            white_board = WbFrame(root, width=1600, height=900, full=True)
        else:
            white_board = WbFrame(root, width=1600, height=900, full=False)

    if args.devmode:
        white_board.draw_grid()

    setup_streams(oAuth_obj)
    pull_tweets(oAuth_obj)
    #white_board.draw_grid()
    root.mainloop()
    kill_streams()
    exit()

def pull_tweets(auth):
    api = API(auth)
    for status in Cursor(api.user_timeline, id="404whiteboard").items(max_tweets/2):
        #tweet_list.append(status)
        white_board.add_tweet_to_board(status)

    #for status in Cursor(api.home_timeline, id="404whiteboard").items(max_tweets): #authenticating user isn't the correct user
        #print(status.text)
        #if "@404whiteboard" in status.text:
            #tweet_list.append(status)

    #white_board.paint_tweets(tweet_list)

def setup_streams(auth):
    twitter_list = WBListener()
    #twitter_list2 = WBListener()
    global stream_obj

    stream_obj = Stream(auth, twitter_list)
    stream_obj.filter(track=['#trump'], async=True)

def kill_streams():
    global stream_obj
    stream_obj.disconnect()

if __name__ == '__main__':
    main()

