
import os

# Another approach avoiding COM is xlwt from python-excel.org.

if os.name == 'nt' :
	from win32com.client import Dispatch    #, constants
	#import win32con as con    #Unused import
	#import win32api, winsound #Unused import
	#import time               #Unused import
	#import numpy as np        #Unused import
else :
	print 'Unable to import nt modules.'

def MakeSheet(wx, tab, spread) :
	# Open excel
	busy = wx.BusyInfo("Creation of spreadsheet in progress ... ", tab)
	wx.Yield()		# necessary, otherwise busyinfo display is empty on Linux.
	excel = Dispatch('Excel.application')
	excel.workbooks.Add()
	sheet = excel.ActiveSheet
	busy.Destroy()
	busy = wx.BusyInfo("Writing data to the spreadsheet ...\n\nThis will take about 11 seconds. ", tab)
	wx.Yield()		# necessary, otherwise busyinfo display is empty on Linux.
	row = 1
	for r in range(len(spread)) :
		row += 1
		col = 1
		addRow(row, spread[r], col, sheet)
		#for c in range(len(spread[r])) :
			#col += 1
			#cell = sheet.Cells(row, col)
			#cell.value = spread[r][c]
	# Delete all knowledge of the excel process for this Python session.
	excel.visible = 1
	#excel.windowState = con.WS_MAXIMIZE
	busy.Destroy()
	del excel

def addRow(row_i, data_tuple, start_col, sheet):
	"""
	Modified from Active State code recipes 528870
	Add row in a single operation.  Takes a tuple per row.
	Much more efficient than cell by cell. http://support.microsoft.com/kb/247412.
	"""
	col_n = len(data_tuple)
	last_col = start_col + col_n - 1
	insert_range = getRangeByCells((row_i, start_col), (row_i, last_col), sheet)
	insert_range.Value = data_tuple

def getRangeByCells((cell_start_row, cell_start_col), (cell_end_row, cell_end_col), sheet):
	"""Get a range defined by cell start and cell end e.g. (1,1) A1 and (7,2) B7"""
	a = sheet.Cells(cell_start_row, cell_start_col)
	b = sheet.Cells(cell_end_row, cell_end_col)
	return sheet.Range(a, b)


def Demo() :
	# Open excel
	excel = Dispatch('Excel.application')
	excel.visible = 1
	#excel.windowState = con.WS_MAXIMIZE
	excel.workbooks.Add()
	sheet = excel.ActiveSheet

	# Specify cell contents

	# Some description of the contents:
	cell = sheet.Cells(1,1)
	cell.value = "Array"
	cell.Font.Size = 14
	cell.Font.Bold = True

	# Enter data row by row.
	data = range(0,10)
	row_start = 3
	rows = 5
	rows = range(row_start, rows + row_start)
	addresses = []          # These cell addresses will be used later.
	for row in rows :
	    column_start = 2
	    cell = sheet.Cells(row, column_start - 1)
	    cell.value = 'Data Set' + str(row - row_start)
	    column = column_start
	    row_addresses = []
	    for item in data :
	        cell = sheet.Cells(row, column)
	        cell.value = item * row
	        row_addresses.append(cell.Address)      # Record the cell address.
	        column += 1
	    addresses.append(row_addresses)


	# Create a 'Total' row and enter a summation formula at the end of each column.
	cell = sheet.Cells(row + 1, column_start - 1)
	cell.value = 'Total'
	# Make sum formulas
	column = column_start
	row += 1
	for item in data :
	    cell = sheet.Cells(row, column)
	    cell.value = '=sum(' + addresses[0][column-column_start] + ":" + addresses[len(addresses)-1][column-column_start] + ')'
	    column += 1

	# Delete all knowledge of the excel process for this Python session.
	del excel

#-------------------------------------------------------------------------------------------
if __name__ == '__main__' :
	Demo()

