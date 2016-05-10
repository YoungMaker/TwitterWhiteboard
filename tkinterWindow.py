# -*- coding: utf8 -*-
__author__ = 'Aaron'
from mtTkinter import Frame, Canvas, Menu
import tkFont
#from tweepy import models
from random import randint
from random import seed
from ref import error_status
from ref import non_printing_chars
import re


class TweetObject():
    status = None
    color = None
    life = 0;
    loc_x = 0
    loc_y = 0
    canvas_text = None

    def __init__(self, status, color, loc_x, loc_y, life=0):
        self.status = status
        self.color = color
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.life = life


    def draw_tweet(self, canvas, dist_x, dist_y):
        delta_x = randint(-5, 5) #no delta x now that font scaling is being implemented?
        delta_y = randint(-5, 5)
        self.canvas_text = canvas.create_text((dist_x/2) + (dist_x*self.loc_x) + delta_x, (dist_y/2) + (dist_y*self.loc_y) + delta_y, font=("Another", 24), fill=self.color,  text="" + self.strip_non_print_chars(self.status.text), width=(dist_x-50), tags="tweets")
        final_size = self.scale_text(canvas, dist_x, dist_y)
        print("drew tweet id: tweets %s at size %d" % (str(self.status.id), final_size))

    def scale_text(self,canvas, dist_x, dist_y): #tweet scaling algorithm
        bounds = canvas.bbox(self.canvas_text)  # returns bound box for text
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        font_size = 20
        font = tkFont.Font(family="Another", size=(-1*font_size))
        while width < (dist_x-50) and height < (dist_y-50):
            font_size += 1
            font.configure(size=(-1*font_size)) #multiplies by neg 1 for px sizing
            canvas.itemconfig(self.canvas_text,font=font)
            bounds = canvas.bbox(self.canvas_text)  #re-calc bounds
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
        return font_size

    def strip_non_print_chars(self, status_text): #strips out HTML encoded symbols from tweets
        status_text = re.sub(r"http\S+", " <LINK> ", status_text) #uses regex expression to strip out twitter t.co links. Source: http://stackoverflow.com/questions/24399820/expression-to-remove-url-links-from-twitter-tweet
        for key in non_printing_chars:
            #print(non_printing_chars[key])
            if key in status_text:
                status_text = status_text.replace(key, non_printing_chars[key])
        return status_text

    def inc_life(self):
        self.life += 1

    def get_life(self):
        return self.life

    def get_x(self):
        return self.loc_x

    def get_y(self):
        return self.loc_y

    def delete_from_UI(self, canvas):
        if self.canvas_text is None:
            return False
            #print("None?")
        else:
           # print("deleted!")
            canvas.delete(self.canvas_text)

class WbFrame(Frame):
    width = 0
    height = 0
    canvas = None
    colors = ["gray11", "red2", "cyan3", "forest green", "dark slate blue", "OrangeRed2"]
    board = []
    max_tweets = 9
    dist_x = 0
    dist_y = 0
    menu = None

    def exit(self):
        self.parent.destroy()

    def __init__(self, parent,  width=0, height=0, max_tweets=9, full=False):
        self.parent = parent
        self.parent.geometry('%dx%d' % (width, height))
        Frame.__init__(self, self.parent, background="white")
        self.parent.title("TK whiteboard")
        self.width = width
        self.height = height
        self.canvas = Canvas(self.parent, width=self.width, height=self.height)
        self.canvas.config(background="white")
        self.canvas.bind("<Button-3>", self.show_menu)
        self.canvas.pack()
        self.dist_x = (width/3)
        self.dist_y = (height/3)
        self.max_tweets = max_tweets
        self.menu = Menu(self.parent, tearoff=0)
        self.menu.add_command(label="exit", command=self.exit)
        if full:
            self.parent.overrideredirect(True) #add this line in when in fullscreen mode

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def draw_grid(self):
        canvas = self.canvas
        dist_x = (self.width/3)
        dist_y = ((self.height)/3)
        print("%d , %d" % (dist_x, dist_y))
        canvas.create_line(dist_x, 0, dist_x, self.height)
        canvas.create_line((2*dist_x), 0, (2*dist_x), self.height)
        canvas.create_line(0, dist_y, self.width, dist_y)
        canvas.create_line(0, (2*dist_y), self.width, (2*dist_y))

        count = 0
        for i in xrange(3):
            for c in xrange(3):
                canvas.create_text((dist_x/2) + (dist_x*c), dist_y-15 + (dist_y*i), text="%d , %d" % (i, c), tag="markup")
                count += 1

    def draw_error(self, err_code):
        for tweet in self.board:
            tweet.delete_from_UI(self.canvas)
        self.canvas.delete("tweets")
        self.canvas.delete('markup')
        self.canvas.create_text(self.width/2, self.height/2, fill="red2", font=("Another", 75), text="API Error \n %s: %s \n :(" % (str(err_code), error_status[err_code]), width=(0.75*self.width), tag="error", justify="center")
        return False

    def paint_tweets(self, tweet_list): #depreciated. do not use
        canvas = self.canvas
        canvas.delete("tweets")
        seed()
        dist_x = (self.width/3)
        dist_y = (self.height/3)

        x = 0
        y = 0
        for status in tweet_list:
            if x == 3:
                x = 0
                y += 1
            if y == 3:
                y =0
            color = self.colors[randint(0, len(self.colors)-1)]
            delta_x = randint(-50,50)
            delta_y = randint(-50,50)
            canvas.create_text((dist_x/2) + (dist_x*x) + delta_x, (dist_y/2) + (dist_y*y) + delta_y, font=("Another", 24), fill=color,  text="" + status.text, width=400, tags="tweets")
            x += 1

    def create_gfx_object(self, status):
        seed()
        rand_x = randint(0, 2)
        rand_y = randint(0, 2)
        color = self.colors[randint(0, len(self.colors)-1)]
        while self.do_coords_exist(self.board, rand_x, rand_y): #moved existence test to function
            rand_x = randint(0, 2)
            rand_y = randint(0, 2)

        print("tweet id: %s stored at %d , %d" % (str(status.id), rand_x, rand_y))

        return TweetObject(status, color, rand_x, rand_y)

    def do_coords_exist(self, tweet_list, coord_x, coord_y): #checks if tile aready occupied
        for tweet in tweet_list:
            if tweet.get_x() == coord_x and tweet.get_y() == coord_y:
                return True

        return False

    def replace_oldest_gfx_object(self, status, old_tweet):
        seed()
        color = self.colors[randint(0, len(self.colors)-1)]
        print("Old tweet id %s replaced at %d , %d " % (str(old_tweet.status.id), old_tweet.get_x(), old_tweet.get_y()))
        return TweetObject(status, color, old_tweet.get_x(), old_tweet.get_y())

    def find_max_life(self):
        max = -100 #maximum tweet age
        max_tweet = None
        for i in xrange(len(self.board)):
            tweet = self.board[i]
            if(tweet.get_life() > max):
                max = tweet.get_life()
                max_tweet = i
        print("maximum tweet age was %d" % max)
        if max < 0:
            return 0
        return max_tweet

    def add_tweet_to_board(self, status):
        for tweet in self.board:
            tweet.inc_life() #increase life counter
        print("there are %d tweets" % len(self.board))

        if len(self.board) < self.max_tweets:
            n_tweet = self.create_gfx_object(status)
            self.board.append(n_tweet)
            n_tweet.draw_tweet(self.canvas, self.dist_x, self.dist_y)
        else:
            max_age_index = self.find_max_life()
            #print("tweets %s" % str(self.board[max_age_index].status.id))
            self.board[max_age_index].delete_from_UI(self.canvas) #deletes old text
            c_tweet = self.replace_oldest_gfx_object(status, self.board[max_age_index])
            self.board[max_age_index] = c_tweet
            c_tweet.draw_tweet(self.canvas, self.dist_x, self.dist_y) #draws that shit