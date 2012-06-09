# -*- coding=gb2312 -*-
import urllib
import urllib2
import cookielib
import httplib
import re
import sys

#����UA,����opener
user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
cookie = cookielib.CookieJar()
cookie_support= urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(cookie_support)
urllib2.install_opener(opener)
headers = {'User-Agent':user_agent,"Keep-Alive":"115"}

#���ȷ���actIndexҳ��
url1 = 'http://59.67.75.254/actIndex.do'
req1 = urllib2.Request(url1,headers)
response1 = opener.open(url1)

#��ȡSessionID
url2 = response1.geturl()
response2 = opener.open(url2)


#����Ҫ�����ľ缯���ƣ����ؾ缯��Ӧ��progid
def searchProgid(name):
    searchUrl = "http://59.67.75.254/actProgSearch.do"
    searchValues = {
        'button_kind':'search',
        'category':'0',
        "keyword":name,
    }
    searchData = urllib.urlencode(searchValues)
    searchReq = urllib2.Request(searchUrl,searchData,headers)
    searchResponse = opener.open(searchReq)
    searchPage = searchResponse.read()
    searchResult = re.findall(r"\?id=\d+",searchPage)
    if searchResult:
        return int(searchResult[-1].split("=")[1])
    else:
        return "None"

#��ȡproid��Ӧ�еļ���
def gettotalvolume(progid):
    volumeUrl = "http://59.67.75.254/actProgInfo.do"
    volumeValues = {
        "id":progid,
    }
    volumeData = urllib.urlencode(volumeValues)
    volumeReq = urllib2.Request(volumeUrl,volumeData,headers)
    volumeResponse = opener.open(volumeReq)
    volumePage = volumeResponse.read()
    volumeResult = re.findall(r'value="\d+"',volumePage)
    return int(volumeResult[-1].split("=")[-1].strip('"'))
  

#��Ҫ�缯��progid�ͼ���
def getDownloadUrl(progid,volume=1):
    downloadUrl = 'http://59.67.75.254/actDownload.do'
    downloadValues = {'volume':volume,
                      'progid':progid
                      }
    downloadData = urllib.urlencode(downloadValues)
    downloadReq = urllib2.Request(downloadUrl,downloadData,headers)
    downloadResponse = urllib2.urlopen(downloadReq)
    downloadPage = downloadResponse.read().decode('gb2312')
    downloadResult = re.findall("'59.67.75.*'",downloadPage)[0].encode('gb2312').split(',')
    urlpre,url,name=str(downloadResult[0]).strip("'") \
                   ,str(downloadResult[1]).strip("'") \
                   ,str(downloadResult[4]).strip("'")

    resourceUrl =  "http://"+urlpre+"2880"+url
    return resourceUrl


if __name__ == "__main__":
    if len(sys.argv)!=2 :
        sys.exit("������Ҫ�ҵĵ�Ӱ����")     
    moviename   = sys.argv[1]
    progid      = searchProgid(moviename)
    if progid != "None":
        totalvolume = gettotalvolume(progid)   
        print moviename+"����"+str(totalvolume)+"����"
        for i in range(0,totalvolume):
            print getDownloadUrl(progid,volume=i+1)
            print "��"+str(i+1)+"��"

    else:
        print "��ҪѰ�ҵ�Ϸ�粻����,�������������"
        
   
