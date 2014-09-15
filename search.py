#-*-coding:utf-8-*-
import glob
import re
import chardet
def main():
	web_files = glob.glob('webfile\\*.*')  #file list 
	keywords = open('keyword.txt','r')
	for key in keywords.readlines():
		if key[-1] =='\n':
			key = key.replace('\n','')
		key = repr(key.decode('utf-8'))[9:]
		key = key.replace('\\','-')
		key = key[:-1]
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
