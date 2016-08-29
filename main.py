#coding=utf-8
import urllib2
import re
import os

savePath = os.path.join(os.getcwd(), 'xImages')
def start(url):
	page = urllib2.urlopen(url)
	html = page.read()
	reg = r'<a class="movie-box" href=".*">'
	movieBoxRE = re.compile(reg)
	tempStr = ''.join(re.findall(movieBoxRE, html))

	print "网址解析成功，开始爬取..."
	linkReg = r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')'
	linkArr = re.findall(linkReg, tempStr, re.I|re.S|re.M)

	if not os.path.exists(savePath):
		os.mkdir(savePath)	# 创建根目录	
	for idx, url in enumerate(linkArr):
		openSingle(idx + 1, url, url.split('/')[-1])
	print "所有页面爬取完成！"

def openSingle(index, url, name):
	page = urllib2.urlopen(url)
	html = page.read()
	reg = r'<a class="sample-box" href=".*">'
	sampleBox = re.compile(reg)
	tempStr = ''.join(re.findall(sampleBox, html))

	print "正在爬去第" + str(index) + "个页面，番号：" + name + "..."
	imgReg = r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')'
	linkArr = re.findall(imgReg, tempStr, re.I|re.S|re.M)
	for url in linkArr:
		fileName = url.split('/')[-1]
		path = os.path.join(savePath, fileName)
		saveImg(url, path)
	if len(linkArr) < 1:
		print name + '没有截图'
	else:
		print name + '所有截图保存完毕，共' + str(len(linkArr)) + '张'

def saveImg(imageURL, fileName):
	u = urllib2.urlopen(imageURL)
	data = u.read()
	f = open(fileName, 'wb')
	f.write(data)
	f.close()

# searchInfo = ""
searchInfo = raw_input('输入搜索信息(不输入则爬取首页)：')
if searchInfo:
	savePath = os.path.join(os.getcwd(), 'xImages-' + searchInfo)
	start("https://www.javbus.com/search/" + searchInfo)
else:
	start("https://www.javbus.com/");
	
