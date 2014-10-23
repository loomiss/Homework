# Required modules: tabbed_plots_graph.py, tabbed_plots_frames.py
# Imports within modules: os, sys, string as s, numpy *, wx, matplotlib, ...

#from tabbed_plots_frames import *
#from tabbed_plots_graph import *
from notebook_plots_graph import *

def MakeContourData(xo, yo) :
    # Create contourable data.
    x = arange(0., 100., 10.)
    y = arange(0., 100., 10.)
    X,Y = meshgrid(x,y)
    U = cos(X/xo)*cos(Y/yo)
    return [X, Y, U]

def MakePlotData(xo) :
    # Create contourable data.
    x = arange(0., 100., 10.)
    y = cos(x/xo)
    return [x, y]

def CustomizeGraph() :
    # Apply plot commands not covered by MakeGraph or GenericOptions.
    plt.grid(True)  # An example

def KillTab(frame) :
    #frame.tab_figure.close()
    frame.tab_panel.Close()

def TestPlotNotebook(caller) :
    app = wx.App()
    f = PlotFrame(title='Plot Notebook Demonstration', size=(800,800))
    data1 = MakeContourData(20., 20.)
    data2 = MakeContourData(30., 30.)
    
    g1 = Graph('contour', [data1], title = 'Contour Test', background='k')
    caller.plot_notebook, caller.plot_canvas = DefineTab(f, [g1], name='Bare Contour')
    
    #"""
    g2 = Graph('contour', [data1], colorbar=True, title =r'$U(x,y)=cos(x/20)cos(y/20)$', titlesize=25, xlabel=r'$x$', ylabel=r'$y$', labelsize=20, text=[58,60,'You are here.'], textsize=8)
    DefineTab(f, [g2], name='Contour With LaTeX')
    
    g3 = Graph('contour', [data1, data2], title = 'Double Contour Plot')    # Two superimposed countour plots
    DefineTab(f, [g1, g2, g3], name='Multiple Contour Subplots', arrangement=[2,2]) # Arrangement does not need to be specified.
    
    data3 = MakePlotData(20.)
    data4 = MakePlotData(30.)
    g4 = Graph('plot', [data3, data4], symbols=['bo','go'], grid=False, title = 'Plot Test', background='w', xlabel=r'$x$', ylabel=r'$cos(x/x_\circ)$', labelsize=25, legend=[r'$x_\circ=20$', r'$x_\circ=30$'], customize=CustomizeGraph)
    DefineTab(f, [g4], name='Simple Plot')
    #"""
    f.Show()
    app.MainLoop()
    # To save a tab as an image, return the tab to its default size before saving.
    # The cursor position display does not function within a subplot in a tab.  It can be made to function by adding the position display to the bottom toolbar somehow.

def Test() :
    app = wx.App(False)
    #raw_input('?')
    f = PlotFrame()
    data1 = MakeContourData(20., 20.)
    data2 = MakeContourData(30., 30.)
    
    g1 = Graph('contour', [data1], title = 'Contour Test', background='k')
    f.tab_to_kill = DefineTab(f, [g1], name='Bare Contour')
    
    #"""
    g2 = Graph('contour', [data1], colorbar=True, title =r'$U(x,y)=cos(x/20)cos(y/20)$', titlesize=25, xlabel=r'$x$', ylabel=r'$y$', labelsize=20, text=[58,60,'You are here.'], textsize=8)
    DefineTab(f, [g2], name='Contour With LaTeX')
    
    g3 = Graph('contour', [data1, data2], title = 'Double Contour Plot')    # Two superimposed countour plots
    DefineTab(f, [g1, g2, g3], name='Multiple Contour Subplots', arrangement=[2,2]) # Arrangement does not need to be specified.
    
    data3 = MakePlotData(20.)
    data4 = MakePlotData(30.)
    g4 = Graph('plot', [data3, data4], symbols=['bo','go'], grid=False, title = 'Plot Test', background='w', xlabel=r'$x$', ylabel=r'$cos(x/x_\circ)$', labelsize=25, legend=[r'$x_\circ=20$', r'$x_\circ=30$'], customize=CustomizeGraph)
    DefineTab(f, [g4], name='Simple Plot')
    #"""
    f.Show()
    app.MainLoop()
    # To save a tab as an image, return the tab to its default size before saving.
    # The cursor position display does not function within a subplot in a tab.  It can be made to function by adding the position display to the bottom toolbar somehow.
    
# --------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    Test()
