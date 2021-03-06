#coding=utf-8
import urllib2
import re
import os

savePath = os.path.join(os.getcwd(), 'xImages')
def start(url, page, startIndex):
	targetURL = url + "/" + str(page)
	html = readSource(url)
	reg = r'<a class="movie-box" href=".*">'
	movieBoxRE = re.compile(reg)
	tempStr = ''.join(re.findall(movieBoxRE, html))

	print "网址解析成功，开始爬取..."
	linkReg = r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')'
	linkArr = re.findall(linkReg, tempStr, re.I|re.S|re.M)

	if not os.path.exists(savePath):
		os.mkdir(savePath)	# 创建根目录	
	for idx, url in enumerate(linkArr):
		if (idx < startIndex):
			continue
		openSingle(idx + 1, url, url.split('/')[-1])
	print "所有页面爬取完成！"

def openSingle(index, url, name):
	html = readSource(url)
	imgReg = r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')'
	reg = r'<a class="sample-box" href=".*">'
	sampleBox = re.compile(reg)
	tempStr = ''.join(re.findall(sampleBox, html))

	coverReg = r'<a class="bigImage" href=".*">'
	cover = re.compile(coverReg)
	coverTempUrl = re.findall(cover, html)[0]
	coverUrl = re.findall(imgReg, coverTempUrl, re.I|re.S|re.M)[0]
	coverExt = '.' + coverUrl.split('.')[-1]
	coverPath = os.path.join(savePath, name + coverExt)
	saveImg(coverUrl, coverPath)

	print "正在爬取第" + str(index) + "个页面，番号：" + name + "..."
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
	data = readSource(imageURL)
	if not data:
		return
	f = open(fileName, 'wb')
	f.write(data)
	f.close()

def readSource(url):
	u = a_urlopen(url)
	fails = 0
	while True:
		try:
			if fails > 3:
				break
			data = u.read()
			return data
		except:
			fails += 1
			print '解析内容失败，正在重试 ',fails,' ',url
	print '无法解析 ',url

def a_urlopen(url):
	fails = 0
	while True:
		try:
			if fails > 10:
				break
			req = urllib2.Request(url)
			response = urllib2.urlopen(req, None, 25)
			return response
		except:
			fails += 1
			print '网络异常，正在重试 ',fails,' ',url
	print '无法访问 ',url

# searchInfo = ""
searchInfo = raw_input('输入搜索信息(默认爬取首页)：')
startIndex = raw_input('输入起始序号（默认1）：')
if not startIndex:
	startIndex = 0
else:
	startIndex = int(startIndex) - 1
if searchInfo:
	savePath = os.path.join(os.getcwd(), 'xImages-' + searchInfo)
	start("https://www.javbus.com/search/" + searchInfo, 1, startIndex)
else:
	start("https://www.javbus.com/page", 1, startIndex)
	
