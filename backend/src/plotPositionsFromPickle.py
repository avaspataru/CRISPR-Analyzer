import pickle
import argparse
import shap
import sys
import matplotlib.pyplot as plt
import numpy as np

from utils import *


def plotPosForFile(fileName):
    #get a list of tuples (avg shap value, feature name). function def in utils
    featureImp = getAvgShapValues(fileName)

    #sort the features by the absolute value of the avg Shap value
    print("Getting positional values...")

    #creates dictionary where average[nucleotide id][position] = the average shap value of the nucleotide being at that position
    averages = getShapValsForPosFeatures(featureImp) #function def in utils

    print("Plotting...")

    width = 0.35 # the width of the bars
    positions = range(0,20)
    pA = plt.bar(positions, averages[0], width)
    pC = plt.bar(positions, averages[1], width)
    pG = plt.bar(positions, averages[2], width)
    pT = plt.bar(positions, averages[3], width)

    plt.xticks(positions)
    plt.plot(range(-1,21), [0]*22, color='black', linewidth=0.5) #plot a line at 0

    plt.ylabel("SHAP values")
    plt.xlabel("Guide positions")
    plt.title("SHAP values for positional features")
    #plt.title("SHAP values for positional features from " + getToolName(fileName).upper() + " ran on the " + getDatasetName(fileName).upper() + " dataset")
    plt.legend((pA[0], pC[0], pG[0], pT[0]), ('A', 'C', 'G', 'T'))

    #plt.savefig('../plots/guide-positions/'+getToolName(fileName).upper() +'-'+ getDatasetName(fileName).lower() )

    return plt
