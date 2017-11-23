#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import re
import datetime

now = datetime.datetime.now()

# page starting HTML
start_page_static = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Nombre de billets disponibles ({tmonth} {tday}, {ttime})</title>
</head>
<!DOCTYPE html>
<html lang="en">
  <body>
	<!-- Table to show data -->
	<table width="100%" border="1" bordercolor="#cccccc" cellpadding="5"
	cellspacing="5">
		<tr>
		 	<th colspan="4">
Nombre de billets disponibles (dernière mise à jour: {month} {day}, {time})
			</th>
		</tr>
		<tr>
		 	<th>Date</th>
			<th>Français</th>
			<th>English</th>
		</tr>
'''

# page ending HTML
end_page_static = '''
    </table>
  </body>
</html>
</html>
'''

# data table format to fit data in it
data_row = '''
		<tr>
			<td>{month} - {date}, {year}</td>
			<td>
				<table width="100%" bordercolor="#cccccc">
					{fre_content}
				</table>
			</td>
			<td>
				<table width="100%" bordercolor="#cccccc">
					{eng_content}
				</table>
			</td>
		</tr>
'''

# check if ticket is avilable or not
def onlyTicket(available_ticket):
	if "tickets" in available_ticket:
		tickets = available_ticket.split(" ")[0]
		if int(tickets) < 5:
			return "-"
		elif int(tickets) > 4:
			return tickets
	else:
		return "-"


def endHTML():
	with open('Ticket_Data_Table.html', 'a') as html_file:
		html_file.write(end_page_static)



def startHTML():
	sps = start_page_static.format(
		tmonth=now.strftime('%b'),
		tday=now.day,
		ttime=str(now.hour)+":"+str(now.minute),
		month=now.strftime('%b'),
		day=now.day,
		time=str(now.hour)+":"+str(now.minute))
	with open('Ticket_Data_Table.html', 'w') as html_file:
		html_file.write(sps)

# writing the collected data to the html file 
def produceHTMLPage(ticket_data):
	startHTML()
	for by_day in ticket_data:
		eng = ''
		fre = ''
		try:
			for one in by_day:
				if 'English' == one.program_language:
					time = '<tr><td>' + one.start_time + '</td>'
					ticket = '<td>' + onlyTicket(one.available_ticket)+ '</td><tr>'
					eng += time + ticket
				elif 'French' == one.program_language:
					time = '<tr><td>' + one.start_time + '</td>'
					ticket = '<td>' + onlyTicket(one.available_ticket)+ '</td><tr>'
					fre += time + ticket
			table_content = data_row.format(
				month=by_day[0].month[:3],
				date=by_day[0].date,
				year=by_day[0].year,
				fre_content=fre,
				eng_content=eng)
			with open('Ticket_Data_Table.html', 'a') as html_file:
				html_file.write(table_content)
		except:
			pass
	endHTML()
