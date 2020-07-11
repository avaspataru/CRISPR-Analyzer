import sys
import numpy as np
import re
import pickle

nucleotides = ['A','C','G','T']

#gets the tool name from the file name given as argument
def getToolName(fileName):
    split = fileName.split('-')
    #without shap and without dataset
    toolName = '-'.join(split[1:-1])
    return toolName

#gets the dataset name from the fileName given as argument
def getDatasetName(fileName):
    split = fileName.split('-')
    dataName = split[-1] #last word in fileName
    return dataName

#for a fiven tool name, gets a shorthand
def getShorthand(tool):
    if tool == 'tuscan-classification':
        return 'tc'
    elif tool == 'tuscan-regression':
        return 'tr'
    elif tool == 'wu-crispr':
        return 'wu'
    elif tool == 'sgrnascorer2':
        return 's2'
    elif tool in ['chop-chop-xu', 'chop-chop-doench', 'chop-chop-moreno']:
        sep = tool.split('-')
        return 'ch-'+sep[2][0] #first letter of the scoring method
    else:
        return tool


#returns the object corresponding to the requested tool
def getToolObject(toolName):
    if toolName in ['tuscan-regression','tuscan-classification']:
        sys.path.insert(0,'./tuscan-model')
        from tuscandata import TuscanData
        tool = TuscanData()
        tool.setRegressionFlag(toolName=='tuscan-regression') #if regression
    elif toolName == 'sgrnascorer2':
        sys.path.insert(0, './sgRNAScorer2-model')
        from sgRNAScorer2data import SgRNAScorer2Data
        tool = SgRNAScorer2Data()
    elif toolName == 'wu-crispr':
        sys.path.insert(0,'./wu-crispr-model')
        from wucrisprdata import WuCrisprData
        tool = WuCrisprData()
    elif toolName == 'ssc':
        sys.path.insert(0, './ssc-model')
        from sscdata import SSCData
        tool = SSCData()
    elif toolName in ['chop-chop-xu', 'chop-chop-doench', 'chop-chop-moreno']:
        #ASSUME Xu scoring method = TO DO CHANGE
        sys.path.insert(0, './chop-chop-model')
        from chopchopdata import ChopChopData
        tool = ChopChopData()
        tool.setScoring(toolName)
    else:
        print("Tool Name not valid")
        quit()
    return tool

#gets the feature names for the tool which was used to produce the pickle file
def getFeatureNames(fileName):

    #get the tool corresponding to the file name
    toolName = getToolName(fileName)
    tool = getToolObject(toolName) #from utils.py

    #get the actual feature names from the tool object
    featureNames = tool.loadFeatureNames()
    return featureNames

#from a given pickle file name
#takes out the shap values of all the data points and averages out by feature
#returns a list of tuples (shap val, feature name)
def getAvgShapValues(fileName):

    #load the SHAP values and the data
    p = open('../results/'+fileName,"rb")
    print("Loading data...")
    shapValues = pickle.load(p)
    dataset = pickle.load(p)
    p.close()

    #feature names for the tool the pickle was created with
    featureNames = getFeatureNames( fileName )

    #calculate the average shap value across all datapoints for a feature
    print("Calculating averages...")
    avgShapVals = [0] * len(featureNames) #initialise

    #shapValues = dataset x features
    for d in range(0,len(dataset)):
        for f in range(0,len(featureNames)):
            avgShapVals[f] = avgShapVals[f] + shapValues[d][f] #add the value from this datapoint

    #average out the sum
    avgShapVals = [ v / len(dataset) for v in avgShapVals]

    featureImp = sorted( zip(avgShapVals,featureNames) , key = lambda t: abs(t[0])) #zip with the feature names and sort
    #featureImp = featureImp[-20:] # take the top 20 highest values <=> most important 20 features
    featureImp = list(reversed(featureImp)) #order from most important to least important

    return featureImp

#given a list of feature importances as tuples (shap val, feature name)
#extracts the positional features (pos:nucleotide)
#and returns a dictionary averages
#where averages[nucleotide][pos] = the shapley value of the feature pos:nucleotide
def getShapValsForPosFeatures(featureImp):
    averages = np.zeros((4,20))#initialise
    matches = 0 #number of positional features found
    for f in featureImp:
        featureValue = f[0] #the shapley value of this feature
        featureName = f[1] #the name of this feature

        if 'PAM' in featureName or '_p' in featureName or '_lf' in featureName or '_rf' in featureName: #ignore because we don't account for pam, right or left positions
            continue

        #matching the feature name to something containing position-nucleotide [only one nucleotide!]
        #(position) (maybe :) (nucleotide) (anything but another nucleotide)
        m = re.match(r"((.*)[^0-9])?(?P<pos>((\d)(\d)*))(:)?(?P<nuc>[ACGT])([^ACGT](.*))?$", featureName)

        if m == None: #maybe the position and nucleotide are in reverse order
            #(something + not a nucleotide or start) (nucleotide) (maybe :) (pos) (not digit + something or end)
            m = re.match(r"^((.*)[^ACGT])?(?P<nuc>[ACGT])(:)?(?P<pos>((\d)(\d)*))([^0-19](.*))?$", featureName)

        if m == None: #not a positional feature
            continue
        matches = matches + 1
        pos = int( (m.group('pos')) )
        nuc = nucleotides.index(m.group('nuc')) # A:0, C:1, G:2, T:3


        averages[nuc][pos] = featureValue

    assert matches <= 80 #can only have 80 positional features

    return averages
