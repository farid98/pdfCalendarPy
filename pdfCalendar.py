from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm 
from reportlab.platypus import  Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER



import os
import datetime
from calendar import monthrange
import calendar

###########################################################################################

individualDateTextBoxSize = (0.7 * cm, 0.7 * cm)
monthPositions = []
days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

# Positions for all the months from the left edge and the top edge, in cm
def setMonthPositions():
	letftMargin = 2.0  * cm 

	verticalGap = (21 * cm  - letftMargin * 2 - individualDateTextBoxSize[0] * 7  )  /  2
	#	leftMargin = ( width - individualDateTextBoxSize[0] * 3 + verticalGap ) / 2 
	row = 0
	for x in range(0,12):
		if x % 3 == 0:
			row += 1
		
		monthPositions.append( ( letftMargin + (x % 3 ) * verticalGap, row * 6.5 * cm + 2 * cm ) )


def fillMonthNames(canvas):
	for x in range(0,12):
		textobject = canvas.beginText()
		textobject.setTextOrigin( monthPositions[x][0] , 7 * individualDateTextBoxSize[0] + A4[1] - monthPositions[x][1]  )
		textobject.setFont("Helvetica", 14)
		textobject.textOut(calendar.month_name[x + 1])
		canvas.drawText(textobject)
 
def coord(x, y, unit=1):
    x, y = x * unit, A4[1] -  y * unit
    return x, y

def printMonth(month, year, x, y, myCanvas):
	monthMatrix= []
	monthMatrix.insert(0,days)  
     
	oneWeekArray = []

	total_days = monthrange(year, month + 1)[1]
	weekStarts = monthrange(year, month + 1)[0]

	date = 0

	#This starts filling out the actual date numerals into an array . This is simply the actual numerals, no sense of spcing eytc. That comes later at printing time.	
	weekStartpadding = 0
	for _  in range(0,6):
		oneWeekArray = []
		for _ in range(1,8):
			weekStartpadding += 1
			if weekStartpadding <= weekStarts:
				oneWeekArray.append(' ')
			else:
				date = date + 1
				if date > total_days :
					break
				oneWeekArray.append(date)
		
		monthMatrix.append(oneWeekArray)	# this is collecting the full month, which will be printed.

	
	t = Table(monthMatrix, 7*[individualDateTextBoxSize[0]], 7*[individualDateTextBoxSize[1]], hAlign='LEFT')   # data now goes into a table, ready for printing. This is where we set alignment etc.
	t.setStyle(TableStyle([
	                       	('TEXTCOLOR',(0,0),(-1,0),colors.red),
	                       	('TEXTCOLOR',(-1,-1),(0,-1),colors.blue),

							('ALIGN',(0,0),(-1,-1),'RIGHT'),
	                       	('VALIGN',(0,-1),(-1,-1),'MIDDLE'),

	                       	##('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
	                       	##('BOX', (0,0), (-1,-1), 0.25, colors.black),

	                       ]))

	t.wrapOn(myCanvas, A4[0], A4[1])
	t.drawOn(myCanvas, *coord(x, y, 1))


###############################################################

def makeYear(year, saveName):

	# saveName = "calendar3.pdf"
	myCanvas = canvas.Canvas(saveName, pagesize=A4)

	row = 0
	setMonthPositions()
	# year = 2019
	for x in range(0,12):
		if x % 3 == 0:
			row += 1
		printMonth(x,year, monthPositions[x][0], monthPositions[x][1], myCanvas )
	myCanvas.setFont( 'Helvetica', 16 )	
	myCanvas.drawCentredString(A4[0] / 2 ,  A4[1] - 1.5 * cm, str(year))
	fillMonthNames(myCanvas)
	myCanvas.save()


#################################################################

makeYear(2020, "calendar2020.pdf")
