from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import csv
import cv2
import datetime
import numpy as np
import re
import string
import sys
import unidecode
import traceback
import webcolors



def timeTaken(startTime, Metric):
	print(Metric.ljust(25," "),datetime.datetime.now()-startTime)
def string_to_words(s):
	s=s.replace("\n"," ")
	s=s.replace(string.punctuation,"")
	s=re.sub("[^\w]"," ",  s).split()
	return s
def get_words(d):
	txt=d.execute_script("return document.body.innerText")
	if txt==None:
		txt=""
	words = string_to_words(str(unidecode.unidecode(txt)))
	return words


def get_word_count(d):
	startTime=datetime.datetime.now()
	words=get_words(d)
	timeTaken(startTime,"Word Count")
	return float(len(words))
def get_text_body_ratio(soup):

	#print "Param2"
	startTime=datetime.datetime.now()
	headers=[]
	for i in range(1,7):
		headers+=soup.findAll("h"+str(i))
	sizeHeaders=[]
	sizeHeaders+=soup.findAll("font",{"size":"3"})
	sizeHeaders+=soup.findAll("font",{"size":"4"})
	sizeHeaders+=soup.findAll("font",{"size":"5"})
	txt=""
	for i in headers:
		txt+=" "+i.text
	for i in sizeHeaders:
		txt+=" "+i.text
	words=[]
	if len(txt)!=0:
		words=string_to_words(str(unidecode.unidecode(txt)))
	#print words
	timeTaken(startTime,"Text Body Ratio")
	return float(len(words))
def get_emph_body_text_percentage(d):

	#print "Param3"
	startTime=datetime.datetime.now()
	boldText = d.find_elements_by_tag_name("b")
	words=[]
	for i in boldText:
		words+= string_to_words(str(unidecode.unidecode(i.text)))
	boldWordCount=len(words)
	try:
		txt=str(unidecode.unidecode(d.execute_script("return document.body.innerText")))
	except:
		txt=str(unidecode.unidecode(d.execute_script("return document.body.textContent")))
	pattern = re.compile("!+")
	exclWordCount=len(re.findall(pattern,txt))

	words=get_words(d)
	capWordCount=0
	for i in words:
		if i==i.upper():
			capWordCount+=1
	timeTaken(startTime,"Emph text Percent")
	#print boldWordCount, exclWordCount, capWordCount
	return boldWordCount + exclWordCount + capWordCount
def get_text_position_changes(s):
	startTime=datetime.datetime.now()
	#print "Param
	elem=s.findAll()
	prev=""
	textPositionChanges=0
	for i in elem:
		try:
			string=str(i["style"])
			if "text-align:"in string:
				align=string.split("text-align:")[1]
				position=align.split(";")[0].strip()
				if position!=prev:
					textPositionChanges+=1
					prev=position
		except:
			pass
	timeTaken(startTime,"Text Positional Changes")
	return textPositionChanges
def get_text_clusters(d):

	#print "Param5"
	startTime=datetime.datetime.now()
	tableText= d.find_elements_by_tag_name("td")+d.find_elements_by_tag_name("table")
	paraText = d.find_elements_by_tag_name("p")
	textClusters=len(tableText)+len(paraText)
	timeTaken(startTime,"Text Clusters")
	return textClusters
def get_visible_links(d):

	#print "Param6"
	startTime=datetime.datetime.now()
	links=d.find_elements_by_tag_name("a")
	visibleLinkCount=0
	for i in links:
		if i.text != "":
			visibleLinkCount+=1
	timeTaken(startTime,"Visible Links")
	return visibleLinkCount
def get_page_size(d):

	#print "Param7"
	startTime=datetime.datetime.now()
	scriptToExecute = "	var performance = 	window.performance ||\
											window.mozPerformance ||\
											window.msPerformance ||\
									 		window.webkitPerformance || {};\
						var network 	= 	performance.getEntries() || {};\
						return network;"
	networkData = d.execute_script(scriptToExecute)
	pageSize=0
	for i in networkData:
		try:
			pageSize+=int(i[u'transferSize'])
		except:
			pass
	timeTaken(startTime,"Page Size")
	return float(pageSize)/1024.0
def get_graphics_size(d):

	#print "Param8"
	startTime=datetime.datetime.now()
	scriptToExecute = "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
	networkData = d.execute_script(scriptToExecute)
	graphicsSize=0.0
	for i in networkData:
		try:
			if i[u'initiatorType']== u'script' or i[u'initiatorType']==u'img' or i['initiatorType']== u'css':
				graphicsSize+=int(i[u'transferSize'])
		except:
			pass
	timeTaken(startTime,"Graphic Size")
	return float(graphicsSize)/1024.0
def get_graphics_count(d):
	startTime=datetime.datetime.now()
	#print "Param9"
	styleSteets=d.find_elements_by_tag_name("style")
	images=d.execute_script("return document.images;")
	graphicsCount=len(styleSteets)+len(images)
	timeTaken(startTime,"Graphics Count")
	return  graphicsCount
def get_color_count(image):
	startTime=datetime.datetime.now()
	c_count=1
	timeTaken(startTime,"Color Count")
	return c_count
def get_font_count(d):
	startTime=datetime.datetime.now()
	fontCount=1
	timeTaken(startTime,"Font Count")
	return fontCount
def getColorfullness(image):
	startTime=datetime.datetime.now()
	(B, G, R) = cv2.split(image.astype("float"))
	rg = np.absolute(R - G)
	yb = np.absolute(0.5 * (R + G) - B)
	(rbMean, rbStd) = (np.mean(rg), np.std(rg))
	(ybMean, ybStd) = (np.mean(yb), np.std(yb))
	stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
	meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
	timeTaken(startTime,"Colourfullness")
	return stdRoot + (0.3 * meanRoot)
def getVisualComplexity(image):
	startTime=datetime.datetime.now()
	visualComplexity=1
	timeTaken(startTime,"Visual Complexity")
	return visualComplexity
def setDriverOptions():
	options 				= Options()
	options.binary_location = "/home/abhiavk/git/mysite/mysiteEnv/bin/chromium-browser"
	chrome_driver_binary	= "/home/abhiavk/git/mysite/mysiteEnv/bin/chromedriver"
	options.add_argument("--headless")
	return	webdriver.Chrome(chrome_options=options)
def getMetrics(num,url):
	st 				= datetime.datetime.now()
	textFilename	= "CorruptUrls.txt"
	csvFilename		= "tempUrlMetrics.csv"
	try:
		driver			= setDriverOptions()
		driver.implicitly_wait(3)
		driver.get(url)
		driver.set_window_size(1024, 768)
		driver.implicitly_wait(10)
		WebDriverWait(driver, timeout=10).until(lambda x: x.find_elements_by_tag_name('body'))
		driver.save_screenshot('screenshot.png')
		image = cv2.imread('screenshot.png')
		imageGrey = cv2.imread('screenshot.png',0)
		page_source=driver.page_source
		soup=BeautifulSoup(page_source,'html.parser')
		#---------------------------------------------------#
		#--------- Web Metric Calculation ------------------#
		#---------------------------------------------------#
		wordCount				= get_word_count(driver)#Parameter 1
		headTextCount			= get_text_body_ratio(soup)#Parameter 2
		emphTextCount			= get_emph_body_text_percentage(driver)#Parameter 3
		textPositionalChanges	= get_text_position_changes(soup)#Parameter 4
		textClusters			= get_text_clusters(driver)#Parameter 5
		visibleLinks			= get_visible_links(driver)#Parameter 6
		pageSize				= get_page_size(driver)#Parameter 7
		graphicsSize			= get_graphics_size(driver)#Parameter 8
		graphicsCount 			= get_graphics_count(driver)#Parameter 9

		colorCount				= get_color_count(image)#Parameter 10
		fontCount				= get_font_count(driver)#Parameter 11
		colourFullness			= getColorfullness(image)#Parameter 12
		visualComplexity		= getVisualComplexity(imageGrey)
		if pageSize==0:
			graphicsPercent=0.0
		else:
			graphicsPercent=graphicsSize*100.0/pageSize

		if wordCount:
			textBodyRatio=headTextCount/wordCount
			emphTextRatio=emphTextCount/wordCount
		else:
			textBodyRatio=0.0
			emphTextRatio=0.0

		tempMetrics=[
					num,\
					url,\
					wordCount,\
					textBodyRatio,\
					emphTextRatio,\
					textPositionalChanges,\
					textClusters,\
					visibleLinks,\
					pageSize,\
					graphicsPercent,\
					graphicsCount,\
					colorCount,\
					fontCount,\
					colourFullness,\
					visualComplexity
			]
		line=tempMetrics
		csvFile		= open(csvFilename,"a+")
		csvWriter	= csv.writer(csvFile)
		csvWriter.writerow(line)
		csvFile.close()
	except:
		print(traceback.format_exc())
		driver		=	setDriverOptions()
		print("Error scraping the Url")
		f2			= open(textFilename,"a+")
		f2.write(url+"\n")
		f2.close()
	print(datetime.datetime.now()-st,"\t\t",datetime.datetime.now(),url)
	return
def main(filename):
	fields			= ["slno","url","p1","p2","p3","p4","p5","p6","p7","p8","p9","p10","p11","p12","p13"]
	csvFilename		= "tempUrlMetrics.csv"
	csvFile			= open(csvFilename,"a+")
	csvWriter		= csv.writer(csvFile)
	csvWriter.writerow(fields)
	csvFile.close()
	csvFile			= open(filename,"r")
	urlFile			= csv.DictReader(csvFile)
	for row in urlFile:
		getMetrics(row['id'],row['urls'])
	csvFile.close()
if __name__=="__main__":
    filename=sys.argv[-1]
    main(filename)
