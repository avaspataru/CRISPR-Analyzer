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
        return 'chop-'+sep[2][0] #first letter of the scoring method
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


#gets the 30-nucleotide sequences from the dataset (Xu / Doench)
def getDataset(datasetName, toolName):
    if datasetName == 'xu':
        #WHERE THE DATASET IS
        INPUT_FILE_NAME = "../datasets/Xu-2015_Is-Efficient.csv"
        GUIDE_INDEX = 4 #column of the guide in the file

        # Used for extracting the guide from the CSV format
        if (toolName in ['tuscan-regression','tuscan-classification']): #Tuscan has a special extraction of data since it uses context around the guide
            GUIDE_START_POS = 10 - 4
            GUIDE_LEN = 23 + 4 + 3 # TUSCAN considers nucleotides 4 upstream, 3 upstream from guide (?=([ACTG]{25}GG[ACTG]{3}))
        elif toolName == 'wu-crispr': #it needs 3 more nucleotides after the guide
            GUIDE_START_POS = 10
            GUIDE_LEN = 23 + 3
        elif toolName == 'ssc': #it doesn't take the PAM
            GUIDE_START_POS = 10
            GUIDE_LEN = 20
        else: #default for all the other tools
            GUIDE_INDEX = 4
            GUIDE_START_POS = 10
            GUIDE_LEN = 23

    elif datasetName =='doench':
        #where the dataset is
        INPUT_FILE_NAME = "../datasets/Doench-2014.csv"
        GUIDE_INDEX = 1 #column of the quide in the file

        #Used for extracting the guide from CSV format
        # Used for extracting the guide from the CSV format
        if (toolName in ['tuscan-regression','tuscan-classification']): #Tuscan has a special extraction of data since it uses context around the guide
            GUIDE_START_POS = 0
            GUIDE_LEN = 23 + 4 + 3 # TUSCAN considers nucleotides 4 upstream, 3 upstream from guide (?=([ACTG]{25}GG[ACTG]{3}))
        elif toolName == 'wu-crispr': #it needs 3 more nucleotides after the guide
            GUIDE_START_POS = 4
            GUIDE_LEN = 23 + 3
        elif toolName == 'ssc': #it doesn't take the PAM
            GUIDE_START_POS = 4
            GUIDE_LEN = 20
        else: #default for all the other tools
            GUIDE_START_POS = 4
            GUIDE_LEN = 23
    else:
        print("Dataset not supported")
        quit()

    #read in sequences
    sequences = []
    with open(INPUT_FILE_NAME, 'r') as fRead:
        # read each line - file contains header and blank footer - then break apart by comma
        for line in [x.split(',') for x in fRead.read().split('\n')[1:-1]]:
            guideSeq = line[GUIDE_INDEX][GUIDE_START_POS:(GUIDE_START_POS + GUIDE_LEN)]
            sequences.append(guideSeq)
    return sequences



# from a given pickle file name
# takes out the shap values of all the data points and averages out by feature
# ONLY considers positional features
# ONLY considers the data points which have the feature value to  1
# returns a list of tuples (shap val, feature name)
def getAvgShapValues(fileName):

    #load the SHAP values and the data
    p = open('../results/'+fileName,"rb")
    print("Loading data...")
    shapValues = pickle.load(p)
    dataset = pickle.load(p)
    p.close()

    #feature names for the tool the pickle was created with
    featureNames = getFeatureNames( fileName )

    #the original sequences
    sequences = getDataset(getDatasetName(fileName),getToolName(fileName))

    #calculate the average shap value across all datapoints for a feature
    print("Calculating averages...")
    avgShapVals = [0] * len(featureNames) #initialise
    howMany = [0] * len(featureNames) #how many points have 1 values for this feature

    #shapValues = dataset x features
    for d in range(0,len(dataset)):
        for f in range(0,len(featureNames)):

            featureName = featureNames[f]
            m = parsePositionalFeature(featureName)

            if m == None: #not a positional feature => get normal average
                avgShapVals[f] = avgShapVals[f] + shapValues[d][f] #add the value from this datapoint
                howMany[f] = -1
                continue

            pos = int( (m.group('pos')) )
            nuc = nucleotides.index(m.group('nuc')) # A:0, C:1, G:2, T:3

            if (sequences[d][pos] == nucleotides[nuc]): #yes, the feature has a 1 value for this data point
                avgShapVals[f] = avgShapVals[f] + shapValues[d][f]
                howMany[f] = howMany[f] + 1


    #average out the sum
    for v in range(0,len(avgShapVals)):
        if howMany[v] == -1: #not positional
            avgShapVals[v] = avgShapVals[v] / len(dataset)
        elif howMany[v] == 0: #no datapoints have positive value
            avgShapVals[v] = 0
        else: #average over positives
            avgShapVals[v] = avgShapVals[v] / howMany[v]


    featureImp = sorted( zip(avgShapVals,featureNames) , key = lambda t: abs(t[0])) #zip with the feature names and sort
    #featureImp = featureImp[-20:] # take the top 20 highest values <=> most important 20 features
    featureImp = list(reversed(featureImp)) #order from most important to least important

    return featureImp



def parsePositionalFeature(featureName):

    if 'PAM' in featureName or '_p' in featureName or '_lf' in featureName or '_rf' in featureName: #ignore because we don't account for pam, right or left positions
        return None

    #matching the feature name to something containing position-nucleotide [only one nucleotide!]
    #(position) (maybe :) (nucleotide) (anything but another nucleotide)
    m = re.match(r"((.*)[^0-9])?(?P<pos>((\d)(\d)*))(:)?(?P<nuc>[ACGT])([^ACGT](.*))?$", featureName)

    if m == None: #maybe the position and nucleotide are in reverse order
        #(something + not a nucleotide or start) (nucleotide) (maybe :) (pos) (not digit + something or end)
        m = re.match(r"^((.*)[^ACGT])?(?P<nuc>[ACGT])(:)?(?P<pos>((\d)(\d)*))([^0-19](.*))?$", featureName)

    return m


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

        m = parsePositionalFeature(featureName)

        if m == None: #not a positional feature
            continue
        matches = matches + 1
        pos = int( (m.group('pos')) )
        nuc = nucleotides.index(m.group('nuc')) # A:0, C:1, G:2, T:3


        averages[nuc][pos] = featureValue

    assert matches <= 80 #can only have 80 positional features

    return averages
