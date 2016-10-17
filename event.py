'''
Created on 16 Eki 2016

@author: mert
'''
class Event:
    def __init__(self, title, content, date=None, place=None):
        self.title = title
        self.date = date
        self.content = content
        self.place = place