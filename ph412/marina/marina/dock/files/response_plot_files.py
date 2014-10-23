
# Description --------------------------------------------------------------------------------------------------------------
# Classes and procedures for parsing data files and plotting with matplotlib.
#
# Name:        response_plot_files.py
# Author:      W. Hetherington, Physics, Oregon State University
# Created:     2009/11/07
# Modified:
# Copyright:   (c) 2009
# License:     No restrictions
#---------------------------------------------------------------------------------------------------------------------------

import os
import string as s
from numpy import *

class DataFromFile :
    def __init__(self, file_path, delim):
        # Expects rows of data: x, y, z, ...
        # Ignores anything after a #.
        # The delimiter is usually a ','.
        # If one row has more entries than the others, then all rows are extended with
        #   obviously fabricated data and a warning is issued.
        # self.data is an array [xvalues, yvalues, ...]
        self.titles = {}
        self.xlabel = ''
        self.ylabels = {}
        self.legend = ''
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.delim = delim
        self.error = ''
        self.warning = ''
        file_contents = self.ReadFile()
        #print self.error
        if self.error == '':
            data_strings = self.FindParameters(file_contents)
        #print self.error
        if self.error == '' :
            self.ProcessFile(data_strings)
        #print self.error

    def ReadFile(self):
        q = ''
        if os.path.isfile(self.file_path) :
            try:
                fin = open(self.file_path, 'r')
                q = fin.readlines()
                fin.close()
            except :
                self.error = 'Fatal error: ' + self.file_path + ' could not be read.  Check permissions.'
        else :
            self.error = 'The path/file ' + self.file_path + ' does not exist.'
            self.error += '  The current working directory is ' + os.getcwd()
        return q

    def FindParameters(self, q) :
        asc = [43, 45, 46] + range(48, 58)
        data = []
        parameters = {'legend': '', 'xlabel': '', 'ylabels': [], 'title': '', 'column_ids': [] }     # Dictionary of parameters values
        for d in q :
            d1 = s.strip(s.split(d, '#')[0])    # ignore comments
            if d1 :
                d1a = s.split(d1, '>') # look for parameters
                if (s.strip(d1a[0]) == '') & (len(d1a) > 1) :      # parameter line must begin with >.
                    d2 = s.split(d1a[1], '=')
                    if len(d2) > 0 :
                        key = s.strip(d2[0]).lower()
                        if (key == 'legend') | (key == 'xlabel') | (key == 'title') :
                            parameters[key] = s.strip(d2[1])
                        elif (key == 'ylabels') | (key == 'column_ids') :
                            d3 = s.split(d2[1], ',')
                            for d4 in d3 :
                                parameters[key].append(s.strip(d4))
                elif ord(d1[0]) in asc :      # The line is data if it begins with 0-9, -, +, or ..
                    data.append(d1)
        self.parameters = parameters
        #print parameters
        #print parameters
        #try :
            #self.legend = parameters['legend']
            #self.title = parameters['title']
            #self.xlabel = parameters['xlabel']
            #self.ylabels = parameters['ylabels']    # a list
            #self.column_ids = parameters['columns']
        if len(data) == 0 :
            self.error = 'Fatal error: no data found in ' + self.file_name
        return data

    def ProcessFile(self, q) :
        data =[]
        columns = -1
        for d in q :
            e = s.split(d, self.delim)
            eee = []
            for ee in e :
                ees = s.strip(ee)
                try:
                    number = float(ees)
                except:
                    self.warning +='Warning!  This data entry is not numeric: ' + ees + '\n'
                    self.warning += 'The missing data value will be replaced by 0.  This might cause the graphing program to crash.\n'
                    number = 0
                eee.append(number)
            if columns == -1 :
                columns = len(eee)
            if len(eee) < columns :
                self.warning +='Warning!  The number of entries per row is not constant.\n'
                self.warning += 'Make up your mind. ' + str(columns) + ' or ' + str(len(eee)) + ' ?\n'
                self.warning += 'Missing data values will be replaced by 1/10 of the minimum value.\n'
                columns = len(eee)
            else :
                columns = len(eee)
            data.append(eee)
        # If a row does not have all the columns of data, fill it with plotable but clearly
        #   fabricated data and cast a warning.
        # First, find the min and max values for each column of data
        for d in data :
            if len(d) == columns :
                # The immutability of a statement like maxi = d requires this mutable approach.
                maxi = []
                mini = []
                for j in range(columns) :
                    maxi.append(d[j])
                    mini.append(d[j])
            break
        for d in data :
            for i in range(columns) :
                try:
                    if d[i] > maxi[i] :
                        maxi[i] = d[i]
                    if d[i] < mini[i] :
                        mini[i] = d[i]
                except :
                    continue
        # Now fill in the missing data with 1/10 the minimum value for that particular column.
        for i in range(len(data)) :
            for j in range(len(data[i]), columns) :
                data[i].append(mini[j]/10.0)
        # Keep data in numpy arrays.
        tdata = transpose(array(data))  # Data is now of the form [xarray, yarray, ...]
        #print 'tdata'
        #print tdata
        #print 'end tdata'
        if len(tdata) == 1 :
            self.data = [range(len(tdata[0])), tdata[0]]
            columns = 2
        else :
            self.data = tdata
        #print self.data
        self.columns = columns
        self.max = array(maxi)
        self.min = array(mini)
        if self.warning :
            print '\n' + self.file_name
            print self.warning
        if self.error :
            print '\n' + self.file_name
            print self.error

def MakeLegends(file_list) :
    legends = []
    for f in file_list :
        if f.parameters['legend'] != '' :
            legends.append(f.parameters['legend'])
        else :
            legends.append(f.file_name)
    return legends

def MakeTitles(file_list) :
    titles = []
    t = ''
    for i in range(len(file_list)) :
        if i > 0 :
            t += ', '
        a = file_list[i].parameters['title']
        if a != '':
            t += a
        else :
            #t += ', ' + file_list[i].file_name
            t += file_list[i].file_name
    #t += ': '
    #print t
    for i in range(1, file_list[0].columns) :
        for f in file_list :
            #print f.file_name
            #print i, f.parameters['column_ids']
            if len(f.parameters['column_ids']) > i-1 :
                if f.parameters['column_ids'][i] != '' :
                    addendum = f.parameters['column_ids'][i]
                    break
            addendum = ''
        titles.append(t + addendum)
    return titles


#---------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__' :
    print
