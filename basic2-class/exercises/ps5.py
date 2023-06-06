"""
Name:
Collaborators:
Time:
"""

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================


def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1

class NewStory:
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

# ======================
# Triggers
# =================


class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        Trigger.__init__(self)
        self.phrase = phrase.lower()
    
    def is_phrase_in(self, text):
        text = text.lower()

        # Splitting a phrase into individual words
        phrase_words_list = self.phrase.split()
        text_words_list = text.split()

        # Removing any special characters within each word in the phrase
        phrase_words_cleaned = [word.strip(string.punctuation) for word in phrase_words_list]
        text_words_cleaned = [word.strip(string.punctuation) for word in text_words_list]
        
        if (len(text_words_cleaned) < len(phrase_words_cleaned)):
            return False
        for i in range(len(text_words_cleaned)):
            if text_words_cleaned[i:i + len(phrase_words_cleaned)] == phrase_words_cleaned:
                return True
        return False

# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, new_story):
        return self.is_phrase_in(new_story.get_title())


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, new_story):
        return self.is_phrase_in(new_story.get_description())

# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
#  Ex: Input: "6 Apr 2003 12:00:00"
class TimeTrigger(Trigger):
    def __init__(self, time_string):
        self.date_time = datetime.strptime(time_string, "%d %b %Y %H:%M:%S") #2003-04-06 12:00:00
    
    def evaluate(self, new_story):
        new_story_time = datetime.strptime(new_story.get_pubdate(), "%Y-%m-%d %H:%M:%S")
        return new_story_time != self.date_time


# Problem 6
class BeforeTrigger(TimeTrigger): 
    def evaluate(self, new_story):
        return super().evaluate(new_story) and new_story_time < self.date_time

class AfterTrigger(TimeTrigger): 
    def evaluate(self, new_story):
        return super().evaluate(new_story) and new_story_time > self.date_time


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
        
    def evaluate(self, new_story):
        return not self.trigger.evaluate(new_story)

# Problem 8
"""
This trigger should take two triggers as arguments to its constructor, 
and should fire on a news story only if both of the inputted triggers would fire on that item.
"""
class AndTrigger(Trigger):
    def __init__(sefl, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = triggere

    def evaluate(self, new_story):
        return self.trigger1.evaluate(new_story) and self.trigger2.evaluate(new_story)

# Problem 9
"""
This trigger should take two triggers as arguments to its constructor, 
and should fire if either one (or both) of its inputted triggers would fire on that item. 
"""
class OrTrigger(Trigger):
    def __init__(sefl, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = triggere

    def evaluate(self, new_story):
        return self.trigger1.evaluate(new_story) or self.trigger2.evaluate(new_story)

# ======================
# Filtering
# ======================


# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    filter_stories = []
    for story in stories:
        for trigger in triggerlist:
            if (trigger.evaluate(story)):
                filter_stories.append(story)
                break
    return filter_stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, "r")
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith("//")):
            line_part = line.split(',')
            line_name = line_part[0].strip()
            line_type = line_part[1].strip()

            if line_type == 'TITLE':
                line_phrase = line_part[2].strip()
                trigger = TittleTrigger(phrase)
            elif line_type == 'DESCRIPTION':
                line_phrase = line_part[2].strip()
                trigger = DescriptionTrigger(phrase)
            elif line_type == 'BEFORE':
                date_time = datetime.strptime(line_part[2].strip(), "%d %b %Y %H:%M:%S")
                trigger = BeforeTrigger(date_time)
            elif line_type == 'AFTER':
                date_time = datetime.strptime(line_part[2].strip(), "%d %b %Y %H:%M:%S")
                trigger = AfterTrigger(date_time)
            elif line_type == 'AND':
                trigger = AndTrigger(line_phrase[2], line_phrase[3])
            elif line_type == 'OR':
                trigger = OrTrigger(line_phrase[2], line_phrase[3])
            elif line_part[0] == 'ADD':
                stories = [t1, t4]
                triggerlist = []
                triggerlist.append(trigger) for trigger in line_part[1:]
                trigger = filter_stories(stories, triggerlist)
            else:
                raise ValueError("Invalid trigger type")
            lines.append(trigger)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines)  # for now, print it so you see what it contains!


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify="center")
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=" ")
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
