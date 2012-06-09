#!/usr/bin/python2
#coding=utf-8
import sys
import json

from bookmark2vimwiki import *
#文件夹信息
#'id':'title'
foldername = {}

#书签信息,文件夹的url=='Folder'
#[父文件夹id，url，title,自己id]
bookmarks = []

#父子文件夹关系
#父id：子id
finaldict =  {}

#调式开关
Debug = False #True

def jsonparse(d):
    """解析出json中的书签，1:将书签保存到bookmark列表中去 2：文件夹信息
    """
    #存储书签
    if d.get(u'type')=='text/x-moz-place':
        bookmarks.append([d.get(u'parent'),d.get(u'uri'),d.get(u'title'),d.get(u'id')])
    #存储文件夹
    if d.get(u'type')=='text/x-moz-place-container':
        if foldername.has_key(d.get(u'id')):
            pass
        else:
            foldername[d.get(u'id')] = d.get(u'title')
            bookmarks.append([d.get(u'parent'),'Folder',d.get(u'title'),d.get(u'id')])
    #遍历子结点
    children = d.get(u'children')
    if children:
        for i in range(len(children)):
            jsonparse(children[i])

def process():
    """主要是处理父子文件夹关系,存放至finaldict字典中"""
    for bookmark in bookmarks[1:]:
       if bookmark[1] == 'Folder':#是文件夹
           #遍历所有文件夹列表，找出和此文件夹
           for fold in foldername.items():
               if fold[0] == bookmark[3]: #没有和自己一样的就就自己，有的就加进来文件夹的id和父文件夹的id相同，即给foldername建立一个父子对照的关系
                   if not finaldict.has_key(str(bookmark[0])):
                       finaldict[str(bookmark[0])] = list([fold[0]])
                   else:
                       finaldict[str(bookmark[0])].append(fold[0])
    if Debug:
       print finaldict
       for i in finaldict.items():
           print 'id:%s ' % i[0]
           print i[1]
 
def output():
    """输出"""
    for folder in foldername.items():
        if folder[0] == 1: #获取了root节点
            pass
        elif folder[0] == 4: #获取了Tag，忽略
            pass
        elif folder[0] == 2: #获取了Bookmark Menu结点
            outputSub(2,'-Bookmarks Menu')
            #pass
        elif folder[0] == 3: #获取了Bookmark Toolbar结点
            outputSub(3,'-Bookmarks Toolbar')
            #pass
        elif folder[0] == 5: #获取了Unsorted结点
            outputSub(5,'-Unsorted Bookmarks')
            pass
        else: #忽略其他结点
            pass

def outputSub(d,path):           
    """Output"""
    Exit = False
    for final in finaldict.items():
        #检查父子关系dict，如果有子文件夹，则递归子文件夹
        if final[0] == str(d):
            #递归子文件夹
            for i in final[1]:
                #如果子文件的title和路径默认一样，则默认不添加此文件的title
                if path.split('-')[-1].strip("") == foldername[i]:
                    outputSub(i,path)
                #添加子文件的title
                else:
                    temppath = path+'-'+foldername[i]        
                    outputSub(i,temppath)
                    temppath = path #恢复
    #此时d没有子文件夹了，则输出d目录下的所有文件
    else:
        print path.encode('utf-8')
        #print "-%s" % foldername[d].encode('utf-8')    
        for bookmark in bookmarks:
            if bookmark[0] == d and bookmark[1]!="Folder":
                print "%s||%s" % (bookmark[2].encode('utf-8'),bookmark[1].encode('utf-8'))

def prin():
    """解析成必要的格式并存储为文本"""
    jsonparse(j)
    process()
    output()

if __name__ == '__main__':
    try:
        s = open('./bookmarks-2011-10-30.json','r').read()
        j = json.loads(s)
    except ValueError, e:
        print >>sys.stderr, 'Could not load JSON object from .'
        sys.exit(1)
    prin()    

    #proc = transform('./unsort.txt')    
    #proc.make()
