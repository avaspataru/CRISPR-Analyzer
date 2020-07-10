
import numpy as np
import pandas as pd
import sys

from tooldata import *

#needed order of nucleotides as defined by the SSC model (A-1, C-2, G-3, T-4)
nucleotides = ['A','C','G','T']


#############################################################################
## Adaptation of C++ code from SSC source code
## See: https://sourceforge.net/projects/spacerscoringcrispr/
############################################################################

class MatrixModel:

    matrix = [[]]

    #Loading a matrix of coefficients which will be used to score the sgRNAs
    def loadMatrix(self):
        matrixFile = open('./ssc-model/human_CRISPRi_20bp.matrix','r')
        lines = matrixFile.readlines()
        lines.pop(0) #skip intercept (at 0)
        lines.pop(0) #skip header (A,C,G,T)
        matrixFile.close()

        matrix = []
        row = 1
        for line in lines: #get the coefficients for position row
            coefs = line.strip().split('\t')
            coefs = [float(coef) for coef in coefs]
            matrix.append(coefs) #store this row of coefficients
            row = row + 1

        self.matrix = matrix

    # For a set of data, to predict a datapoint simply add up the coefficients
    # Expects data to have the features (i.e. if at position 1 there is A, C, G, T; if at position 2.... and etc.)
    def predict(self, data):
        results = []
        for d in data:
            score = 0 #intercept is at 0
            #one data point is a list of features (0-80)
            for f in range(0,20): #position f
                for n in range(0,4): #the nth nucleotide
                    #one feature is if the nucleotide is there
                    if(d[f*4 + n] == 1): #this nucleotide is present in position f
                        score = score + self.matrix[f][n] #add the coefficient
            results.append(score)

        return np.array(results)

#############################################################################
## This class defines the necessary code for the SSC tool to be called in
## by the shapvals.py script.
############################################################################
class SSCData(ToolData):

    #the training set is the Xu dataet
    def loadTrainingSet(self):
        xuFile = open('../datasets/Xu-2015_Is-Efficient.csv')
        GUIDE_INDEX = 4
        GUIDE_START_POS = 10
        GUIDE_LEN = 20

        sequences = []

        # read each line - file contains header and blank footer - then break apart by comma
        for line in [x.split(',') for x in xuFile.read().split('\n')[1:-1]]:
            guideSeq = line[GUIDE_INDEX][GUIDE_START_POS:(GUIDE_START_POS + GUIDE_LEN)]
            sequences.append(guideSeq)
        xuFile.close()

        #compute the features for the training set sequences
        feature_set = []
        for g in sequences:
            features = self.getFeatures(g)
            feature_set.append(features)

        #put the features in a dataframe
        df = pd.DataFrame(feature_set)
        return df

    #the features are whether a position has a specific nucleotide
    def loadFeatureNames(self):
        names = []
        for i in range(0,20): #20bp
            for n in nucleotides:
                names.append(str(i) + ":" + n)
        return names

    #the model of the SSC tool is defined in MatrixModel class above
    def loadModel(self):
        model = MatrixModel()
        model.loadMatrix()
        return model

    #Returns the feature set for a given nucleotide sequence
    def getFeatures(self,seq):
        features = []
        for s in seq:
            for n in nucleotides: #feature is a flag for nucleotide at position
                if(s == n):
                    features.append(1)
                else:
                    features.append(0)
        return features
