#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import time
import TicketDetails
from lxml import html
from Table import produceHTMLPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

reload(sys)
sys.setdefaultencoding('utf8')


# Wait until calander and data loaded for 10 seconds
def wait():
	try:
		myElm = WebDriverWait(browser, 60).until(
			EC.presence_of_element_located((
				By.XPATH, './/td[@class="next"]')))
	except Exception as e:
		raise e
	try:
		myElm = WebDriverWait(browser, 10).until(
			EC.presence_of_element_located((By.XPATH,
				'//div[@class="closed-event-toggler"]'+
				'/following-sibling::table//tr')))
	except Exception as e:
		raise e


# get the next date js code use to go for next date
def getNextJSCode():
	jscode = browser.find_element_by_xpath(
		'.//td[contains(@class,"selected")]').get_attribute('class')
	if "sunday" in jscode:
		return browser.find_element_by_xpath(
			'.//td[contains(@class,"selected")]/ancestor::tr' +
			'/following-sibling::tr[1]/td[1]/a'
			).get_attribute('href').split("'")[1]
	if "sunday" not in jscode:
		return browser.find_element_by_xpath(
			'.//td[contains(@class,"selected")]/following-sibling::td[1]/a'
			).get_attribute('href').split("'")[1]



def getTicketData():
	by_date = []
	pgsource = browser.page_source
	tree = html.fromstring(pgsource)
	
	current_date = tree.xpath('.//td[contains(@class,"selected")]/a/text()')[0]
	current_month = tree.xpath('.//div[@class="calendar-title"]/text()'
		)[0].split('. ')[1]
	current_year = tree.xpath('.//div[@class="calendar-title"]/text()'
		)[0].split('. ')[0]
	visitcount = len(tree.xpath('.//div[@class="closed-event-toggler"]/'+
		'following-sibling::table//tr[contains(@style,"display: none;")=false]'
		))
	for i in range(1, int(visitcount)):
		try:
			eng_or_fre = tree.xpath('.//div[@class="closed-event-toggler"]/'+
				'following-sibling::table//tr[' + str(i) +
				']//div[@class="artist"]/text()')[0]
		except:
			continue
		if eng_or_fre == 'in English' or eng_or_fre == 'in French':
			available_ticket = tree.xpath('.//div[@class="closed-event-'+
				'toggler"]/following-sibling::table//tr[contains(@style,'+
				'"display: none;")=false][' + str(i) +
				']//div[@class="buborek"]/text()')[0]
			language = eng_or_fre.split(' ')[1]
			start_time = tree.xpath('.//div[@class="closed-event-toggler"]/'+
				'following-sibling::table//tr[' + str(i) +
				']//div[@class="time-slice-top"]/text()')[0]
			by_date.append(
				TicketDetails.TicketDetail(
					current_date,
					current_month,
					current_year,
					available_ticket,
					language,
					start_time))
	return by_date



def main():
	day_count = 0
	print "getting : "
	print "https://www.jegymester.hu/eng/Production/480000/Parlamenti-latogatas"
	browser.get(
		'https://www.jegymester.hu/eng/Production/480000/Parlamenti-latogatas')
	by_date = getTicketData()
	while True:
		day_count = day_count + 1
		if day_count <= 30:
			print "day : ",day_count
			ticket_data.append(by_date)
			by_date = []
			try:
				njscode = getNextJSCode()
				browser.execute_script("javascript:doRefresh('"+njscode+"')")
				try:
					wait()
					by_date = getTicketData()
				except:
					print 'There\'s no ticket available for this day'
			except Exception as e:
				break
		else:
			break
	# write data to the html file
	produceHTMLPage(ticket_data)
	browser.close()
	print """************* RUN COMPLETED SUCCESSFULLY *************"""



if __name__ == '__main__':
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	browser = webdriver.Chrome(chrome_options=chrome_options)
	ticket_data = []
	by_date = []
	main()
