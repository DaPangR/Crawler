#-*-coding:utf-8-*-
from os.path import dirname, exists, isdir,isfile, splitext
import os
import glob
import re
import chardet
import urllib2
import urlparse

class Retriever(object):
	def __init__(self,url):
		if url[-1] == '/':
			url = url[:-1]
		self.url = url
		print url
		parse = urlparse.urlparse(url)
		if parse[2] != '':
			name = parse[2].split('/')
			if name[-1] == '/':
				name = name[-2]+ '.html'
				#print '1'
			else:
				if '.' not in name[-1]:
					name = name[-1] + '.html'
					#print '2'
				else:
					name= name[-1]
					#print '3'
		else:
			name = parse[1] + '.html'
			#print '4'
		path = os.getcwd()
		if not isdir(path+'\\webfile'):
			os.makedirs(path+'\\webfile')
		self.filename = path +'\\webfile\\'+name
		print 'filename is:'+self.filename
		self.patt = "http://[\w]+\.[\w-]+\.[\w\/\.-\?=:]+"          #匹配链接的正则表达式，原创，准确性不高
		
	def download(self):
		try:
			print self.url+' is downloading...'
			if isfile(self.filename):
				return "this web page have existed,don't need download"
			html_1 = urllib2.urlopen(self.url,timeout=120).read()
		except IOError:
			retval = ('*** ERROR: invalid URL "%s"' % self.url,)
			return retval  
		except:
			pass
		mychar=chardet.detect(html_1)    #检查该网页是什么编码
		bianma=mychar['encoding']   
		if bianma == 'utf-8' or bianma == 'UTF-8':   
			html=html_1   
		else :   
			html =html_1.decode('gb2312','ignore').encode('utf-8')
		try:
			file = open(self.filename,'wb')
			file.write(self.url+'\n')
			file.write(html)
			file.close()
		except IOError:
			retval = '*** ERROR: file create error!!'
		retval = self.url +' have Done!'
		return retval
		
	def getlinks(self):
		file = open(self.filename,'r').read()
		links = re.findall(self.patt,file)      #返回链接列表
		del links[0]            #因为每个网页头一行，被写成该网页的网址，所以要将列表中的第一个链接删除
		return links
	
class Spider(object):
	def __init__(self,url,num = 0):
		self.queue = [url]      #未访问的
		self.seen = []  #已经访问过的
		self.dom = urlparse.urlparse(url)[1].split('.')[1]+'.'+urlparse.urlparse(url)[1].split('.')[2] 
		#网站的主域名，防止爬到外站
	def getPage(self,url):
		r=Retriever(url)
		retval=r.download()
		self.seen.append(url)
		print retval            #显示下载结果
		print 
		if retval[0][0] == '*': #如果出错
			#print retval
			return
		links = r.getlinks()
		for eachlink in links:  #there need more code
			if self.dom not in eachlink:    #如果这条链接不包含主域名
				continue
			if eachlink not in self.seen:
				self.queue.append(eachlink)
	def go(self):
		while self.queue:
			url = self.queue.pop()
			temp = url.split('.')[-1]
			if not (('cn' in temp) or ('com' in temp) or ('html' in temp) or ('htm' in temp) or ('html' in temp)): 
				print url + ' is not a url'
				continue
			if url in self.seen:
				continue
			self.getPage(url)
				
	
def main():
	path=os.getcwd()
	link_file = open(path + os.sep+'link.txt','r')
	spiders = []                    #通过这个可以知道文件提供了多少个网址
	for eachLink in link_file.readlines():
		eachLink = eachLink.replace('\n','')            #将每行网址末尾的\n去掉
		s = Spider(eachLink)
		spiders.append(s)
		s.go()
	link_file.close()   
	
	web_files = glob.glob('webfile\\*.*')  #下载到的网页文件列表
	keywords = open('keyword.txt','r')
	for key in keywords.readlines():
		if key[-1] =='\n':
			key = key.replace('\n','')
		key = repr(key.decode('utf-8'))[9:]     #将编码转换成unicode字符串,并去掉前面9个unicode说明符？
		key = key.replace('\\','-')             #将unicode中的\\转换为-，因为用\\不支持正则
		key = key[:-1]                          #去掉unicode最后的一个',为了可读性（以后自己能看懂），这里分开成3行写
		for one_web_file_name in web_files:
			file = open(one_web_file_name,'r')
			text = repr(file.read().decode('utf-8')).replace('\\','-')      #将文件内容读出，译码成unicode，转换成字符串，将\\替换成-
			if repr(re.search(key,text)) != 'None': 	        #这里应该有更好地方法，但是目前没想到
				file.seek(0)
				print file.readline()
			file.close()
	print 'all Done'
		
if __name__ == '__main__':
	main()
