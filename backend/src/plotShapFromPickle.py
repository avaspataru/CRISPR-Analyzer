import pickle
import argparse
import shap


def plotShapForFile(fileName):
    #load the SHAP values and the data
    p = open('../results/'+fileName,"rb")
    print("Loading data...")
    shap_values = pickle.load(p)
    dataset = pickle.load(p)
    p.close()

    #plot
    print("Plotting...")
    return (shap_values, dataset)
