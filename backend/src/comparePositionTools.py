import matplotlib.pyplot as plt
from utils import *
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)



def compareMethods(methods):
    #setting up for plotting
    positions = range(0,20)
    x = np.arange(len(positions))  # the label locations
    width = 0.8  # the width of the bars together
    barwidth = width / len(methods) #the width of a single bar
    spacer = (1-width) / len(methods)
    fig, ax = plt.subplots()

    #add separators for each position in the guide
    for p in range(0,21):
        plt.axvline(x=p, color="black",linewidth=0.2)

    tool_positions = [] #where the tool name is to be placed
    tool_labels = [] #what the tool name is

    #plotting data method by method
    cnt = 0
    for method in methods:
        #load data from pickle
        pickleFileName = "SHAP-" + method
        tool = getToolName(pickleFileName)
        data = getDatasetName(pickleFileName)

        #get a list of tuples (avg shap val, feature name)
        featureImp = getAvgShapValues(pickleFileName)
        #creates dictionary where average[nucleotide id][position] = the average shap value of the nucleotide being at that position
        averages = getShapValsForPosFeatures(featureImp) #function def in utils

        #plot the values of each nucleotide at x_coord
        x_coord = x + spacer + barwidth/2 + barwidth*cnt
        pA = ax.bar(x_coord, averages[0], barwidth, color="#1f77b4")
        pC = ax.bar(x_coord, averages[1], barwidth, color="#ff7f0e")
        pG = ax.bar(x_coord, averages[2], barwidth, color="#2ca02c")
        pT = ax.bar(x_coord, averages[3], barwidth, color="#d62728")

        #add the name of the tool under each bar [will use the two arrays for this later]
        for xp in x_coord:
            tool_positions.append(xp)
            tool_labels.append( getShorthand(tool)+"-"+data[0] )

        cnt = cnt+1

    #plot names of tools at the bottom
    plt.xticks(tool_positions, tool_labels, rotation='vertical')

    #plot the number of the guide position at the top
    ax_t = ax.secondary_xaxis('top')
    ax_t.tick_params(axis='x', direction='out', width=0, length=0, color="#D3D3D3")
    ax_t.set_xticks([p + 0.5 for p in positions])
    ax_t.set_xticklabels(positions)

    #plot a line at 0
    plt.plot(range(-1,21), [0]*22, color='black', linewidth=0.2)


    plt.ylabel("SHAP values")
    plt.title("Guide positions")
    plt.legend((pA[0], pC[0], pG[0], pT[0]), ('A', 'C', 'G', 'T'))


    return plt
