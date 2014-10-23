
# Description --------------------------------------------------------------------------------------------------------------
# Classes and procedures for parsing data files and plotting with matplotlib.
#
# Name:        response_plot_base.py
# Author:      W. Hetherington, Physics, Oregon State University
# Created:     2009/11/07
# Modified:
# Copyright:   (c) 2009
# License:     No restrictions
#---------------------------------------------------------------------------------------------------------------------------

from numpy import *
#import matplotlib  #Unused import
#try:
    #import wx
    #matplotlib.use('WXAgg') # The recommended way to use wx is with the WXAgg backend.
#except :
    #print 'wx not found.'
#from matplotlib.figure import Figure
from matplotlib import pyplot as plt

def DefineFigureOld(x, y_sets, grid=True, title=None, legends=None, xlabel=None, ylabel=None, symbol='o') :
    # X must be a single array for the x axis.
    # Y must be an array of y arrays.
    f = plt.figure()
    sb = f.add_subplot(111)
    for i in range(len(y_sets)) :
        if legends :
            label_string = legends[i]
        else :
            label_string = ''
        sb.plot(x, y_sets[i], symbol, label=label_string)
    if xlabel : plt.xlabel(xlabel)
    if ylabel : plt.ylabel(ylabel)
    if legends : sb.legend()
    if grid : sb.grid()
    if title : plt.title(title)
    #if legend: sb.legend()
    return

def DefineFigure(xy_sets,grid=True, title=None, legend=None, xlabel=None, ylabel=None, symbols=['', '', '', '', '']) :
    # xy_sets is a set of [x,y] pairs of arrays
    # X must be an array of x arrays.
    # Y must be an array of y arrays.
    #error = ''     #Unused Variable
    f = plt.figure()
    sb = f.add_subplot(111)
    for i in range(len(xy_sets)) :
        if legend :
            label_string = legend[i]
        else :
            label_string = ''
        sb.plot(xy_sets[i][0], xy_sets[i][1], symbols[i], label=label_string)
    if xlabel : plt.xlabel(xlabel, fontsize=14)
    if ylabel : plt.ylabel(ylabel, fontsize=14)
    if legend : sb.legend()
    if grid : sb.grid()
    if title : plt.title(title)
    #if legend: sb.legend()
    return

def PlotTestOld() :
    x=array(range(10))
    y = power(x,2)
    f = DefineFigureOld(x, [y], title='y=power(x,3)', xlabel='x', ylabel='y')      #Unused Variable
    x2=array(range(1,5))
    y2 = power(x2,3)
    f2 = DefineFigureOld(x2, [y2], title='y=power(x,3)', xlabel='x', ylabel='y')
    plt.show()

def PlotTest() :
    x1=array(range(10))
    y1 = power(x1,2)
    x2=array(range(1,5))
    y2 = power(x2,3)
    f = DefineFigure([[x1,y1], [x2,y2]], title='y=power(x,3)', xlabel='x', ylabel='y')
    plt.show()

#---------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__' :
    PlotTest()
