import sys
import yaml

import MakePDFCal as PDFCal


if (__name__ == '__main__'):

	# Deal with the command line arguments...
	if (len(sys.argv) == 4):
		year       = int (sys.argv[1])
		month      = -1
		paramFile  = sys.argv[2]
		outputFile = sys.argv[3]
	elif (len(sys.argv) == 5):
		year       = int (sys.argv[1])
		month      = int (sys.argv[2])
		paramFile  = sys.argv[3]
		outputFile = sys.argv[4]
	else:
		print ('ERROR: Not enough input parameters')
		print ('')
		print (f'USAGE: {sys.argv[0]} <YEAR> <PARAMETER FILE> <OUTPUT FILE>')
		print (f'       {sys.argv[0]} <YEAR> <MONTH> <PARAMETER FILE> <OUTPUT FILE>')
		print ('')
		exit ()


	# Load the parameter file if it exists...
	try:
		paramFilePtr = open (paramFile)
	except IOError:
		print (f'ERROR: Could not open file... {paramFile}')
		exit ()

	
	# Load and parse the parameter file
	calParams = yaml.load (paramFilePtr, Loader=yaml.FullLoader)


	# finally make the calendar
	if (month != -1):
		PDFCal.MakePDFMonthCal (year, month, calParams, outputFile)
	else:
		PDFCal.MakePDFYearCal (year, calParams, outputFile)



