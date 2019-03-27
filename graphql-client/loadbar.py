import math
import sys

class LoadBar:

    def __init__(self, width, quantity):
        self.count = 0
        self.width = width
        self.part = math.ceil(width / quantity)

    def init(self, message):
        print(message)
        sys.stdout.write("-%s-" % ("-" * self.width))
        sys.stdout.write("\b" * (self.width + 1))
        sys.stdout.flush()
    
    def write(self, quantitiy):
        sys.stdout.write("%s" % ("█" * quantitiy))
        sys.stdout.flush()
    
    def increase(self):    
        self.count = self.count + self.part
        if self.count >= self.width:
            self.write(self.part - (self.count - self.width))
            print('\n')            
        else:
            self.write(self.part)