from tooldata import ToolData
from collections import defaultdict
from sklearn.svm import SVC

import pandas as pd
import numpy as np

class SgRNAScorer2Data(ToolData):


    #########################################################################
    ## This class contains extracted code from the source of SgRNAScorer 2
    ## see https://sgrnascorer.cancer.gov/
    ##
    ## The extracted code has been split into different methods to fit in
    ## the ToolData interface
    #########################################################################

    # binary encoding
    encoding = defaultdict(str)
    encoding['A'] = '0001'
    encoding['C'] = '0010'
    encoding['T'] = '0100'
    encoding['G'] = '1000'

    # add encoding for ambiguous bases
    encoding['K'] = '1100'
    encoding['M'] = '0011'
    encoding['R'] = '1001'
    encoding['Y'] = '0110'
    encoding['S'] = '1010'
    encoding['W'] = '0101'
    encoding['B'] = '1110'
    encoding['V'] = '1011'
    encoding['H'] = '0111'
    encoding['D'] = '1101'
    encoding['N'] = '1111'


    #Initialising
    training_data = pd.DataFrame(np.array([]))
    training_target = np.array([])

    #Fitting the model to the loaded training data
    #Assumes training data has been loaded
    def loadModel(self):
        # model is a linear support vector classifier
        clfLinear = SVC(kernel='linear')
        clfLinear.fit(self.training_data,self.training_target)
        return clfLinear

    #Returns an array of the 80 feature names
    def loadFeatureNames(self):
        #each data point has 80 features 0/1 => whether it has the nucleotide in that position
        features_names = []
        nucleotide_names = ['G','T','C','A'] #in order of encoding left to right
        for i in range(0,20): #20 base pairs
            for j in range(0,4): #4 nucleotides
                name = str(i) + ":" + nucleotide_names[j]
                features_names.append(name)
        return features_names

    #The training set are the two support vectors
    #High = efficient ; Low = inefficient
    #Method extracted from originak code
    def loadTrainingSet(self):
        goodFile = open('./sgRNAScorer2-model/Cas9.High.tab','r')
        badFile =  open('./sgRNAScorer2-model/Cas9.Low.tab','r')
        spacerLength = 20
        pamLength = 3

    	# make a giant x list and y list
        xList = []
        yList = []
        offset = 0
        # if the spacer length provided is > 20, only take up to 20 bases
        if int(spacerLength) >= 20:
            spacerLengthInt = 20
            offSetGuide = int(spacerLength) - 20
        else:
            spacerLengthInt = int(spacerLength)
            offSetGuide = 0

        # calculate offSet for SVM
        if int(spacerLength) < 20:
            offSetModel = 20 - spacerLengthInt
        else:
            offSetModel = 0

        # go through each list
        for sequence in goodFile:
            sequence = sequence.rstrip('\r\n')
            entryList = []
            x = offSetModel
            while x < spacerLengthInt + offSetModel:
                y = 0
                while y < 4:
                    entryList.append(int(self.encoding[sequence[x]][y]))
                    y += 1
                x += 1
            xList.append(entryList)
            yList.append(1)

        # go through the bad
        for sequence in badFile:
            sequence = sequence.rstrip('\r\n')
            entryList = []
            x = offSetModel
            while x < spacerLengthInt + offSetModel:
                y = 0
                while y < 4:
                    entryList.append(int(self.encoding[sequence[x]][y]))
                    y += 1
                x += 1
            xList.append(entryList)
            yList.append(-1)

        # close files
        goodFile.close()
        badFile.close()

        self.training_data = pd.DataFrame(np.array(xList))
        self.training_target = np.array(yList)

        return self.training_data


    #Compute the feature set for a given sequence
    def getFeatures(self,seq):
        # the features are a 0 or 1 whether the nucleotides are in the position or not

        nucleotide_names = ['G','T','C','A'] #in order of encoding left to right

        pos = 0 #index for the features array
        features = [0] * 80

        for i in range(0,20): #20 base pairs
            for j in range(0,4): #4 nucleotides
                #check if the jth nucleotide is at position i
                features[pos] = 0
                if seq[i] == nucleotide_names[j]:
                    features[pos] = 1
                pos = pos + 1

        return features
