import calendar

from fpdf import FPDF


INCH_TO_POINT        = 72
NUMBER_WEEKDAYS      =  7

YEAR_MONTH_ROWS_PORT = 4
YEAR_MONTH_COLS_PORT = 3

YEAR_MONTH_ROWS_LAND = 3
YEAR_MONTH_COLS_LAND = 4

SUNDAY               = 'S'
PORTRAIT             = 'P'

GRID_ROWS            = 6

MAX_FONT_SCALE       = 512
MAX_WIDTH_ITERS      = 15
MAX_NUMBER_STR       = '00'
MAX_WEEKDAY_STR      = 'WEDNESDAY'


#
# FindMaxFontHeight
# - finds the maximum height of some text based on a certain font and font style and a 
#   maximum width
#
def FindMaxFontHeight (Font, FontStyle, BaseHeight, MaxWidth, MaxTestString):

	fontScale = MAX_FONT_SCALE
	fontWidth = 0
	fontSize  = 0

	pdfFile = FPDF (orientation=PORTRAIT, unit='in', format='letter')

	for i in range (1, MAX_WIDTH_ITERS):

		fontScale1 = fontScale - MAX_FONT_SCALE / (2 ** i)
		fontScale2 = fontScale + MAX_FONT_SCALE / (2 ** i)

		pdfFile.set_font (Font, style=FontStyle, size=fontScale1 * BaseHeight)
		testFontWidth1 = pdfFile.get_string_width (MaxTestString)

		pdfFile.set_font (Font, style=FontStyle, size=fontScale2 * BaseHeight)
		testFontWidth2 = pdfFile.get_string_width (MaxTestString)

		sizeDifference1 = abs (MaxWidth - testFontWidth1)
		sizeDifference2 = abs (MaxWidth - testFontWidth2)

		#print (i, fontScale1, testFontWidth1, sizeDifference1)
		#print (i, fontScale2, testFontWidth2, sizeDifference2)

		if (sizeDifference1 < sizeDifference2):
			fontScale = fontScale1
			fontWidth = testFontWidth1
			fontSize  = fontScale1 * BaseHeight
		else:
			fontScale = fontScale2
			fontWidth = testFontWidth2
			fontSize  = fontScale2 * BaseHeight

	return (fontScale, fontWidth, fontSize)



#
# MakePDFMonthCal
# - Quite a big function that does all the calendar making, that is
#   writing the appropriate elements to a PDF file.
# - This is not the best piece of code... will be improved in the next version
#
def MakePDFMonthCal (year, month, calParams, outputFile):

	startMonth = 1
	endMonth   = 12
	
	# Create a calendar instance
	if (calParams ['FirstDay'] == SUNDAY):
		cal = calendar.Calendar (calendar.SUNDAY)
	else:
		cal = calendar.Calendar (calendar.MONDAY)


	pdfFile = FPDF (orientation=calParams['PageOrientation'], unit='in', format='letter')

	pdfFile.add_page()
	pdfFile.set_left_margin (calParams['PageXOrigin'])
	pdfFile.set_top_margin  (calParams['PageYOrigin'])

	calXOffset = 0
	calYOffset = 0
	calMonth   = month

	fontStyle = ''
	if (calParams['FontBold'] == True):
		fontStyle += 'b'
	if (calParams['FontItalic'] == True):
		fontStyle += 'i'

	calHeight = calParams['PageHeight']
	calWidth  = calParams['PageWidth']
	numCols   = 1
	numRows   = 1

	if (month == -1):
	
		pdfFile.set_draw_color (calParams['DebugColourR'], calParams['DebugColourG'], calParams['DebugColourB'])
		pdfFile.set_line_width (calParams['DebugLineThickness'])

		pdfFile.set_xy (calParams['PageXOrigin'], calParams['PageYOrigin'])
		pdfFile.set_font (calParams['Font'], style=fontStyle, size=INCH_TO_POINT*calParams['YearHeader']) 
		pdfFile.set_text_color (calParams['FontColourR'], calParams['FontColourG'], calParams['FontColourB'])
		pdfFile.cell (calWidth-calParams['YearGridSpacing'], calParams['YearHeader'], txt=str(year), border=calParams['Debug'], align='C')

		calParams['PageYOrigin'] += (calParams['YearHeader'] + calParams['YearHeaderSpace'])

		if (calParams['PageOrientation'] == PORTRAIT):
			calHeight = (calParams['PageHeight'] - calParams['YearHeader'] - calParams['YearHeaderSpace']) / YEAR_MONTH_ROWS_PORT
			calWidth  = calParams['PageWidth']  / YEAR_MONTH_COLS_PORT

			numCols = YEAR_MONTH_COLS_PORT
			numRows = YEAR_MONTH_ROWS_PORT
		else:
			calHeight = (calParams['PageHeight'] - calParams['YearHeader'] - calParams['YearHeaderSpace']) / YEAR_MONTH_ROWS_LAND
			calWidth  = calParams['PageWidth']  / YEAR_MONTH_COLS_LAND

			numCols = YEAR_MONTH_COLS_LAND
			numRows = YEAR_MONTH_ROWS_LAND

		calHeight -= calParams['YearGridSpacing']
		calWidth  -= calParams['YearGridSpacing']

	else:

		startMonth = month
		endMonth   = month


	for calMonth in range (startMonth, endMonth+1):

		if (calParams['Debug']):
			pdfFile.set_draw_color (calParams['DebugColourR'], calParams['DebugColourG'], calParams['DebugColourB'])
			pdfFile.set_line_width (calParams['DebugLineThickness'])
			pdfFile.rect (calParams['PageXOrigin'] + calXOffset, calParams['PageYOrigin'] + calYOffset, calWidth, calHeight)

		#
		# Make title...
		#

		pdfFile.set_text_color (calParams['FontColourR'], calParams['FontColourG'], calParams['FontColourB'])

		if (calParams['TitleStyle'] == 1):

			pdfFile.set_xy (calParams['PageXOrigin'] + calXOffset, calParams['PageYOrigin'] + calYOffset)
			pdfFile.set_font (calParams['Font'], style=fontStyle, size=INCH_TO_POINT*calParams['BlockMonthTitleHeight']*calHeight) 
			pdfFile.cell (calWidth, \
			              calParams['BlockMonthTitleHeight']*calHeight, \
	        		      txt=calendar.month_name[calMonth], \
		        	      border=calParams['Debug'], align='C')


		elif (calParams['TitleStyle'] == 2):

			pdfFile.set_font (calParams['Font'], style=fontStyle, size=INCH_TO_POINT*calParams['BlockMonthTitleHeight']*calHeight)
			monthFontWidth = pdfFile.get_string_width (calendar.month_name[calMonth])
			yearFontWidth = pdfFile.get_string_width (str(year))

			pdfFile.set_xy (calParams['PageXOrigin'] + calXOffset, calParams['PageYOrigin'] + calYOffset)
			pdfFile.cell (monthFontWidth, calParams['BlockMonthTitleHeight']*calHeight + calYOffset,\
			              txt=calendar.month_name[calMonth], border=calParams['Debug'], align='L')

			pdfFile.set_xy (calParams['PageXOrigin'] + calXOffset + calWidth - yearFontWidth, calParams['PageYOrigin'] + calYOffset)
			pdfFile.cell (yearFontWidth, calParams['BlockMonthTitleHeight']*calHeight + calYOffset,\
			              txt=str(year), border=calParams['Debug'], align='R')


		#
		# Weekday titles...
		#
		dayIndices = list ( range (0, NUMBER_WEEKDAYS) )
		if  (calParams ['FirstDay'] == SUNDAY):
			dayIndices.insert (0, NUMBER_WEEKDAYS-1)
			dayIndices.pop ()

		fontScaleFactor, fontMaxWidth, fontMaxSize = FindMaxFontHeight (calParams['Font'], fontStyle, \
		                                                                calParams['BlockDayTitleHeight'] * calHeight, \
      	        	                                                        calWidth/NUMBER_WEEKDAYS, \
	                	                                                MAX_WEEKDAY_STR)

		for day in range (0, NUMBER_WEEKDAYS):

			pdfFile.set_xy (calParams['PageXOrigin'] + calXOffset + calWidth * day / NUMBER_WEEKDAYS, \
					calParams['PageYOrigin'] + calYOffset + (calParams['BlockMonthTitleHeight'] + calParams['BlockTitleSpace']) * calHeight)
			pdfFile.set_font (calParams['Font'], style=fontStyle, size=fontScaleFactor*calParams['BlockDayTitleHeight']*calHeight)

			if (calParams['DayTitleStyle'] == 1):
				pdfFile.cell (calWidth / NUMBER_WEEKDAYS, calParams['BlockDayTitleHeight'] * calHeight, \
				              txt=calendar.day_name[dayIndices[day]], border=calParams['Debug'], align='C')
			elif (calParams['DayTitleStyle'] == 2):
				pdfFile.cell (calWidth / NUMBER_WEEKDAYS, calParams['BlockDayTitleHeight'] * calHeight, \
				              txt=calendar.day_name[dayIndices[day]], border=calParams['Debug'], align='L')


		# Horizontal Lines
		if (calParams['HorizontalLines'] == True):

			pdfFile.set_line_width (calParams['HorizontalLineThickness'])
			pdfFile.set_draw_color (calParams['HorizontalLineColourR'], calParams['HorizontalLineColourG'], calParams['HorizontalLineColourB'])

			HorizontalLineAmount = calParams['HorizontalLineSpacing'] * GRID_ROWS

			for row in range (0, HorizontalLineAmount + 1):

				lineXStart = calParams['PageXOrigin'] + calXOffset
				lineXEnd   = calParams['PageXOrigin'] + calXOffset + calWidth
				lineYStart = calParams['PageYOrigin'] + calYOffset + calHeight \
				                                      - (row / HorizontalLineAmount) * calParams['BlockDayRegionHeight'] * calHeight
				lineYEnd   = lineYStart

				pdfFile.line (lineXStart, lineYStart, lineXEnd, lineYEnd)


		# boxes...
		if (calParams['DayGridStyle'] == 4):

			pdfFile.set_line_width (calParams['GridLineThickness'])
			pdfFile.set_draw_color (calParams['DayRegionColourR'], calParams['DayRegionColourG'], calParams['DayRegionColourB'])
			gridOffset = calParams['DayGridSpacing']

			for col in range (0, NUMBER_WEEKDAYS):
				for row in range (0, GRID_ROWS):

					boxXStart = calParams['PageXOrigin'] + calXOffset + (col / NUMBER_WEEKDAYS) * calWidth + gridOffset
					boxXEnd   = calWidth / NUMBER_WEEKDAYS - 2*gridOffset
					boxYStart = calParams['PageYOrigin'] + calYOffset + (1 - calParams['BlockDayRegionHeight']) * calHeight \
					                                     + calParams['BlockDayRegionHeight'] * calHeight * row / GRID_ROWS + gridOffset
					boxYEnd   = calParams['BlockDayRegionHeight'] * calHeight / GRID_ROWS - 2*gridOffset

					drawStyle = 'D'
					if (calParams['DayGridInvert'] == True):
						pdfFile.set_fill_color (calParams['FontColourR'], calParams['FontColourG'], calParams['FontColourB'])
						drawStyle = 'F'	

					pdfFile.rect (boxXStart, boxYStart, boxXEnd, boxYEnd, style=drawStyle)

		# circles
		if (calParams['DayGridStyle'] == 5 or calParams['DayGridStyle'] == 6):

			pdfFile.set_line_width (calParams['GridLineThickness'])
			pdfFile.set_draw_color (calParams['DayRegionColourR'], calParams['DayRegionColourG'], calParams['DayRegionColourB'])
			gridOffset = calParams['DayGridSpacing']

			for col in range (0, NUMBER_WEEKDAYS):
				for row in range (0, GRID_ROWS):

					boxXStart = calParams['PageXOrigin'] + calXOffset + (col / NUMBER_WEEKDAYS) * calWidth + gridOffset
					boxXEnd   = calWidth / NUMBER_WEEKDAYS - 2*gridOffset
					boxYStart = calParams['PageYOrigin'] + calYOffset + (1 - calParams['BlockDayRegionHeight']) * calHeight \
					                                     + calParams['BlockDayRegionHeight'] * calHeight * row / GRID_ROWS + gridOffset
					boxYEnd   = calParams['BlockDayRegionHeight'] * calHeight / GRID_ROWS - 2*gridOffset

					dX = boxXEnd
					dY = boxYEnd

					minBoxXStart = maxBoxXStart = boxXStart
					minBoxXEnd   = maxBoxXEnd   = boxXEnd
					minBoxYStart = maxBoxYStart = boxYStart
					minBoxYEnd   = maxBoxYEnd   = boxYEnd

					if (dX < dY):
						offset = (dY - dX) / 2
						minBoxYStart += offset
						minBoxYEnd   -= (2*offset)
						maxBoxXStart -= offset
						maxBoxXEnd   += offset
					else:
						offset = (dX - dY) / 2
						minBoxXStart += offset
						minBoxXEnd   -= (2*offset)
						maxBoxYStart -= offset
						maxBoxYEnd   += (2*offset)

					drawStyle = 'D'
					if (calParams['DayGridInvert'] == True):
						pdfFile.set_fill_color (calParams['FontColourR'], calParams['FontColourG'], calParams['FontColourB'])
						drawStyle = 'F'	

					pdfFile.ellipse (minBoxXStart, minBoxYStart, minBoxXEnd, minBoxYEnd, style=drawStyle)

					if (calParams['DayGridStyle'] == 6):
						pdfFile.ellipse (boxXStart, boxYStart, boxXEnd, boxYEnd)


		##
		## numbers
		##
		if (calParams['Debug']):
			pdfFile.set_draw_color (calParams['DebugColourR'], calParams['DebugColourG'], calParams['DebugColourB'])
			pdfFile.set_line_width (calParams['DebugLineThickness'])

			
		fontScaleFactor, fontMaxWidth, fontMaxSize = FindMaxFontHeight (calParams['Font'], fontStyle, \
		                                                                calParams['BlockDayRegionHeight'] * calHeight / GRID_ROWS, \
      	        	                                                        calParams['DayFontScale'] * calWidth / NUMBER_WEEKDAYS,
	                	                                                MAX_NUMBER_STR)


		gridOffset = 0
		if (calParams['DayNumPlacement'] == 2):

			gridOffset += max (calParams['DayCornerOffset'] * calWidth / NUMBER_WEEKDAYS, \
			                   calParams['DayCornerOffset'] * calParams['BlockDayRegionHeight'] * calHeight / GRID_ROWS)

		if (calParams['DayGridStyle'] == 4):
			gridOffset += calParams['DayGridSpacing']

		if (calParams['DayGridInvert'] == True):
			pdfFile.set_text_color (255, 255, 255)
		else:
			pdfFile.set_text_color (calParams['FontColourR'], calParams['FontColourG'], calParams['FontColourB'])


		# iterate over all the days in the month
		col = 0
		row = 0
		for i in cal.itermonthdays (year, calMonth):

			# if it is a day within the month, not from the previous or next month then display it
			if (i != 0):
	
				# Central placement	
				if (calParams['DayNumPlacement'] == 1):	

					numberXLoc = calParams['PageXOrigin'] + calXOffset + col / NUMBER_WEEKDAYS * calWidth
					numberYLoc = calParams['PageYOrigin'] + calYOffset + (1 - calParams['BlockDayRegionHeight']) * calHeight \
					                                      + (row / GRID_ROWS) * calParams['BlockDayRegionHeight'] * calHeight \
					                                      + calParams['BlockDayRegionHeight'] * calHeight / (2 * GRID_ROWS) \
					                                      + gridOffset

					pdfFile.set_xy (numberXLoc, numberYLoc)
					pdfFile.set_font (calParams['Font'], style=fontStyle, size=fontScaleFactor*calParams['BlockDayRegionHeight'] * calHeight / GRID_ROWS)
					pdfFile.cell (calWidth/NUMBER_WEEKDAYS, 0, txt=str(i), align='C', border=calParams['Debug'])

				# Corner placement
				elif (calParams['DayNumPlacement'] == 2):
			
					numberXLoc = calParams['PageXOrigin'] + calXOffset + col / NUMBER_WEEKDAYS * calWidth 
					numberYLoc = calParams['PageYOrigin'] + calYOffset + (1 - calParams['BlockDayRegionHeight']) * calHeight \
					                                      + (row / GRID_ROWS) * calParams['BlockDayRegionHeight'] * calHeight 

					if (calParams['HorizontalLines'] == True):
						pdfFile.set_fill_color (255, 255, 255)
						pdfFile.rect (numberXLoc, numberYLoc, fontMaxWidth + 3*gridOffset, fontMaxSize / INCH_TO_POINT + 3*gridOffset, style='F')
	
					numberXLoc += gridOffset
					numberYLoc += gridOffset

					pdfFile.set_xy (numberXLoc, numberYLoc)
					pdfFile.set_font (calParams['Font'], style=fontStyle, size=fontScaleFactor*calParams['BlockDayRegionHeight'] * calHeight / GRID_ROWS)
					pdfFile.cell (fontMaxWidth, fontMaxSize / INCH_TO_POINT, txt=str(i), align='L', border=calParams['Debug'])

			col += 1
			if (col % 7 == 0):
				col = 0
				row += 1

		if (calParams['Debug']):
			pdfFile.set_draw_color (calParams['DayRegionColourR'], calParams['DayRegionColourG'], calParams['DayRegionColourB'])
			pdfFile.set_line_width (calParams['GridLineThickness'])

		##
		## grid
		##

		pdfFile.set_draw_color (calParams['DayRegionColourR'], calParams['DayRegionColourG'], calParams['DayRegionColourB'])
		pdfFile.set_line_width (calParams['GridLineThickness'])

		# horizontal grid lines
		if (calParams['DayGridStyle'] == 1 or calParams['DayGridStyle'] == 2):

			for row in range (0, GRID_ROWS+1):

				lineXStart = calParams['PageXOrigin'] + calXOffset
				lineXEnd   = calParams['PageXOrigin'] + calXOffset + calWidth
				lineYStart = calParams['PageYOrigin'] + calYOffset + calHeight - (row / GRID_ROWS) * calParams['BlockDayRegionHeight'] * calHeight
				lineYEnd   = lineYStart

				pdfFile.line (lineXStart, lineYStart, lineXEnd, lineYEnd)

		# vertical grid lines
		if (calParams['DayGridStyle'] == 1 or calParams['DayGridStyle'] == 3):

			for day in range (0, NUMBER_WEEKDAYS+1):

				lineXStart = calParams['PageXOrigin'] + calXOffset + calWidth - (day / NUMBER_WEEKDAYS) * calWidth
				lineXEnd   = lineXStart
				lineYStart = calParams['PageYOrigin'] + calYOffset + (1 - calParams['BlockDayRegionHeight']) * calHeight
				lineYEnd   = calParams['PageYOrigin'] + calYOffset + calHeight

				pdfFile.line (lineXStart, lineYStart, lineXEnd, lineYEnd)


		if (calMonth % numCols == 0):
			calXOffset = 0
			calYOffset += (calHeight + calParams['YearGridSpacing'])
		else:
			calXOffset += calWidth
			calXOffset += calParams['YearGridSpacing']


	pdfFile.output (outputFile)

	return 0



#
# MakePDFYearCal
# - A year calendar uses the month calendar function.  By setting -1 as the month, a for loop
#   to go through all the months.
#
def MakePDFYearCal (year, calParams, outputFile):

	MakePDFMonthCal (year, -1, calParams, outputFile)

	return 0


