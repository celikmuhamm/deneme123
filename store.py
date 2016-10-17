'''
Created on 16 Eki 2016

@author: mert
'''
class Store:
    def __init__(self):
        self.events = {}
        self.last_event_id = 0

    def add_event(self, event):
        self.last_event_id += 1
        self.events[self.last_event_id] = event
        event._id = self.last_event_id

    def delete_event(self, event_id):
        del self.events[event_id]

    def get_event(self, event_id):
        return self.events[event_id]

    def get_events(self):
        return self.events