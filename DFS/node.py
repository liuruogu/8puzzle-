__author__ = 'liu'
class Node(object):

    def __init__(self, name):
        self.name = name;
        self.adjacenciesList = [];
        self.visited = False;
