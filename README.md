# PyCal

A very simple Python PDF Calendar program.  Instead of using someone elses program, I thought about making one myself.

## Usage

The month, year, parameter and output file are specified are command line arguments.  That is for a monthly calendar: 

> python MakeCal.py [YEAR] [MONTH] [PARAMETER FILE] [OUTPUT FILE]

or for a yearly calendar:

> python MakeCal.py [YEAR] [PARAMETER FILE] [OUTPUT FILE]

for example:

> python MakeCal.py 2020 5 params.yaml MonthMay.pdf

> python MakeCal.py 2020 params.yaml Year2020.pdf
