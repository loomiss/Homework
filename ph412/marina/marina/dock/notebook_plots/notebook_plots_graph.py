
from numpy import *
from notebook_plots_base import *

def DefineTab(frame, graphs, name=None, arrangement=None) :
    # Graphs is graphs, which themselves could consist of multiple, overlayed plots.
    # Name is the name of the tab
    # Arrangement = [rows, columns] specifies the presentation of multiple graphs.  The default is [sqrt(len(data)), sqrt(len(data))].
    if name :
        tab, nb, canvas = frame.AddTab(name)     # tab is actually a figure, and nb is the notebook.
    else :
        tab, nb, canvas = frame.AddTab()
    # Determine the layout.
    layout = 'default'
    warning = ''
    if arrangement:
        if len(arrangement) != 2 :
            warning += 'Warning! Arrangement list should be of the form [rows, columns].  Default arrangement will be used.'
        else :
            rows = int(arrangement[0])
            cols = int(arrangement[1])
            if len(graphs) > rows * cols :
                warning += 'Warning! Arrangement list specifies fewer graphs than the number of data sets.  Default arrangement will be used.'
            else :
                layout = 'custom'
    if warning : print(warning)
    if layout == 'default' :
        rows = int(sqrt(len(graphs)))
        cols = rows
        if len(graphs) > rows * cols :
            rows += 1
            cols += 1
    base = rows*100 + cols*10
    for i in range(len(graphs)) :
        if graphs[i].background :
            tab.add_subplot(base+i+1, axisbg=graphs[i].background)     # Since subplot is derived from the axes class, the axes methods work here.
        else :
            tab.add_subplot(base+i+1)     # Since subplot is derived from the axes class, the axes methods work here.
        p = MakeGraph(graphs[i])
    return nb, canvas       # Return the notebook and canvas backend renderer

def MakeGraph(graph) :
    # Graph is an object with a list of data sets to be plotted on the same graph and other options.
    gr = s.strip(graph.graph).lower()
    i = 0
    for d in graph.data:
        if gr == 'plot' :
            if graph.symbols :
                p = plt.plot(d[0], d[1], graph.symbols[i])
                i += 1
            else :
                p = plt.plot(d[0], d[1])
            GenericOptions(graph)
        elif gr == 'contour' :
            p = plt.contour(d[0], d[1], d[2])
            if graph.colorbar : plt.colorbar()
            GenericOptions(graph)
    return p

def GenericOptions(graph) :
    # Incomplete
    plt.grid(graph.grid)
    if graph.title :
        if graph.titlesize :
            plt.title(graph.title, fontsize=graph.titlesize)
        else :
            plt.title(graph.title)
    if graph.xlabel:
        if graph.labelsize :
            plt.xlabel(graph.xlabel, fontsize=graph.labelsize)
        else :
            plt.xlabel(graph.xlabel)
    if graph.ylabel:
        if graph.labelsize :
            plt.ylabel(graph.ylabel, fontsize=graph.labelsize)
        else :
            plt.ylabel(graph.ylabel)
    if graph.legend :
        plt.legend(graph.legend)
    if graph.text:
        if graph.textsize :
            plt.text(graph.text[0], graph.text[1], graph.text[2], fontsize=graph.textsize)
        else :
            plt.text(graph.text[0], graph.text[1], graph.text[2])
    #if graph.ticklabelsize :
        #plt.xtick.labelsize = graph.ticklabelsize #does not work
        #plt.rc('ticks', xtick.labelsize=graph.ticklabelsize)
    if graph.customize :
        graph.customize()


class Graph :
    def __init__(self, graph, data, symbols=None, styles=None, colors=None, grid=False, title=None, titlesize=None, xlabel=None, ylabel=None, labelsize=None,
             ticklabelsize = None, colorbar=None, background=None, text=None, textsize=None, legend=None, customize=None) :
        # Customize is a hook to a routine to customize the plot.
        # Incomplete
        self.data = data
        self.graph = graph
        self.symbols = symbols      # a list of symbols: ['o', ''] for default color circles and lines,  or ['bo, 'go'] for blue and green circles
        self.styles = styles
        self.colors = colors
        self.grid = grid
        self.title = title
        self.titlesize = titlesize
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.labelsize = labelsize
        self.ticklabelsize = ticklabelsize
        self.colorbar = colorbar
        self.background = background
        self.text = text
        self.textsize = textsize
        self.legend = legend
        self.customize = customize
