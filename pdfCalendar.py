from reportlab.lib.pagesizes import A4, cm
from reportlab.platypus import  Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
import os


monthSize = (0.7 * cm, 0.7 * cm)

xx = []

MonthNumDays = [31,28,31,30,31,30,31,31,30,31,30,31]
width, height = A4
days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
MonthNames = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]


def zeller( day, month, year):
	temp = 0 
	yr1 = 0 
	yr2 = 0
	if month < 3:
		month += 10
		year -= 1
	else:
		month -=2

	yr1 = year/100
	yr2 = year % 100
	temp = (26 * month - 1 ) / 10
	return( (day + temp + yr2 + yr2/4 + yr1/4 - 2*yr1 + 49) % 7 )


# Positions for all the months
def setMonthPositions():
	row = 0
	for x in xrange(0,12):
		if x % 3 == 0:
			row += 1
		
		xx.append( (1.2 + (x % 3) * 6.5, row * 6.5 + 2) )

def fillYearTitle(year, canvas):
	textobject = canvas.beginText()
	textobject.setTextOrigin( 10 * cm,  height - 1 * cm )
	textobject.setFont("Helvetica", 14)
	textobject.textOut(str(year))
	canvas.drawText(textobject)


def fillMonthNames(canvas):
	for x in xrange(0,12):
		textobject = canvas.beginText()
		textobject.setTextOrigin( xx[x][0] * cm, 7 * monthSize[0] + height - xx[x][1] * cm )
		textobject.setFont("Helvetica", 14)
		textobject.textOut(MonthNames[x])
		canvas.drawText(textobject)
 
def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

def printMonth(month, year, x, y):
	data= []
	data.insert(0,days)       
	d = []

	total_days = MonthNumDays[month]
	if ((month == 1) and (year % 4 == 0) and (year % 400 != 0)):
 		total_days += 1      # for leap years, february has one extra day 

	date = 0
	weekStarts = zeller(1, month + 1, year) - 1   
	if weekStarts == -1:
		weekStarts = 6

	weekStartpadding = 0
	for i in range(0,6):
		d = []
		for kount in xrange(1,8):
			weekStartpadding += 1
			if weekStartpadding <= weekStarts:
				d.append(' ')
			else:
				date = date + 1
				if date > total_days :
					break
				d.append(date)
		
		data.append(d)	

	
	t=Table(data,7*[monthSize[0]], 7*[monthSize[1]], hAlign='LEFT')
	t.setStyle(TableStyle([
	                       	('TEXTCOLOR',(0,0),(-1,0),colors.red),
	                       	('TEXTCOLOR',(-1,-1),(0,-1),colors.blue),

							('ALIGN',(0,0),(-1,-1),'RIGHT'),
	                       	('VALIGN',(0,-1),(-1,-1),'MIDDLE'),

	                       	##('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
	                       	##('BOX', (0,0), (-1,-1), 0.25, colors.black),

	                       ]))

	t.wrapOn(c, width, height)
	t.drawOn(c, *coord(x, y, cm))


###############################################################


saveName = "calendar.pdf"
c = canvas.Canvas(saveName, pagesize=A4)

row = 0
setMonthPositions()
year = 2018
for x in xrange(0,12):
	if x % 3 == 0:
		row += 1
	printMonth(x,year, xx[x][0], xx[x][1] )
fillYearTitle(year, c)
fillMonthNames(c)
c.save()



