#!/usr/bin/env python
# -*- coding=utf-8 -*-

class transform:
    
    def __init__(self,file):
        self.filename = file

   def make(self):
        f=open(self.filename,'r')
        for line in f.readlines():
            if line.strip().startswith('U'):
                pass
            else:
                print "["+line.strip().split("||")[-1]+' '+line.strip().split("||")[0]+"]"
