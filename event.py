'''
Created on 16 Eki 2016

@author: mert
'''
class Event:
    def __init__(self, title, event_id, date=None, place=None):
        self.title = title
        self.date = date
        self.place = place
        self.event_id=event_id
        
        
class Image:
    def __init__(self, event_id, image_id, content, date=None):
        self.event_id = event_id
        self.image_id = image_id
        self.date = date
        self.content = content
        
        
class Document:
    def __init__(self, event_id, document_id, content, title, date=None):
        self.event_id = event_id
        self.document_id = document_id
        self.date = date
        self.content = content
        self.title = title