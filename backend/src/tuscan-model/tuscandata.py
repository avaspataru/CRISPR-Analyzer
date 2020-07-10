import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.externals import joblib
import numpy as np
import argparse
from collections import OrderedDict, namedtuple
from tooldata import ToolData

class TuscanData(ToolData):

    is_regression = False

    #to determine if the current object will run the regression model or the classification model
    def setRegressionFlag(self,flag):
        self.is_regression = flag

    ##############################################################################################
    ## EXTRACTED CODE
    ## The following methods needed for the prediction are extracted from the original TUSCAN code
    ## See: https://github.com/BauerLab/TUSCAN
    ##############################################################################################

    NucleotideLocation = namedtuple('NucleotideLocation', ['nucleotide', 'location'])

    DinucleotideLocation = namedtuple('DinucleotideLocation', ['dinucleotide', 'location'])

    REGRESSION_NUCLEOTIDES_OF_INTEREST = (
        NucleotideLocation(nucleotide='T', location=4),
        NucleotideLocation(nucleotide='C', location=7),
        NucleotideLocation(nucleotide='C', location=10),
        NucleotideLocation(nucleotide='T', location=17),
        NucleotideLocation(nucleotide='C', location=20),
        NucleotideLocation(nucleotide='T', location=20),
        NucleotideLocation(nucleotide='G', location=21),
        NucleotideLocation(nucleotide='T', location=21),
        NucleotideLocation(nucleotide='G', location=22),
        NucleotideLocation(nucleotide='T', location=22),
        NucleotideLocation(nucleotide='C', location=24),
        NucleotideLocation(nucleotide='G', location=24),
        NucleotideLocation(nucleotide='T', location=24)
    )

    CLASSIFICATION_NUCLEOTIDES_OF_INTEREST = (
        NucleotideLocation(nucleotide='G', location=5),
        NucleotideLocation(nucleotide='T', location=11),
        NucleotideLocation(nucleotide='C', location=12),
        NucleotideLocation(nucleotide='A', location=16),
        NucleotideLocation(nucleotide='T', location=17),
        NucleotideLocation(nucleotide='C', location=20),
        NucleotideLocation(nucleotide='T', location=20),
        NucleotideLocation(nucleotide='T', location=22),
        NucleotideLocation(nucleotide='T', location=23),
        NucleotideLocation(nucleotide='C', location=24),
        NucleotideLocation(nucleotide='G', location=24),
        NucleotideLocation(nucleotide='T', location=24),
    )

    REGRESSION_DINUCLEOTIDES_OF_INTEREST = (
        DinucleotideLocation(dinucleotide='AC', location=1),
        DinucleotideLocation(dinucleotide='AC', location=2),
        DinucleotideLocation(dinucleotide='CA', location=3),
        DinucleotideLocation(dinucleotide='TT', location=4),
        DinucleotideLocation(dinucleotide='GA', location=5),
        DinucleotideLocation(dinucleotide='CT', location=6),
        DinucleotideLocation(dinucleotide='AC', location=8),
        DinucleotideLocation(dinucleotide='CC', location=8),
        DinucleotideLocation(dinucleotide='GA', location=8),
        DinucleotideLocation(dinucleotide='TT', location=9),
        DinucleotideLocation(dinucleotide='AT', location=10),
        DinucleotideLocation(dinucleotide='CG', location=11),
        DinucleotideLocation(dinucleotide='GA', location=12),
        DinucleotideLocation(dinucleotide='CC', location=14),
        DinucleotideLocation(dinucleotide='GA', location=15),
        DinucleotideLocation(dinucleotide='CC', location=16),
        DinucleotideLocation(dinucleotide='GG', location=16),
        DinucleotideLocation(dinucleotide='TT', location=16),
        DinucleotideLocation(dinucleotide='CT', location=17),
        DinucleotideLocation(dinucleotide='AA', location=18),
        DinucleotideLocation(dinucleotide='GG', location=19),
        DinucleotideLocation(dinucleotide='AT', location=20),
        DinucleotideLocation(dinucleotide='CC', location=20),
        DinucleotideLocation(dinucleotide='CG', location=20),
        DinucleotideLocation(dinucleotide='CT', location=20),
        DinucleotideLocation(dinucleotide='GG', location=20),
        DinucleotideLocation(dinucleotide='TA', location=21),
        DinucleotideLocation(dinucleotide='TG', location=21),
        DinucleotideLocation(dinucleotide='CC', location=22),
        DinucleotideLocation(dinucleotide='GA', location=22),
        DinucleotideLocation(dinucleotide='TA', location=22),
        DinucleotideLocation(dinucleotide='CG', location=23),
        DinucleotideLocation(dinucleotide='GA', location=23),
        DinucleotideLocation(dinucleotide='GG', location=23),
        DinucleotideLocation(dinucleotide='TG', location=23),
        DinucleotideLocation(dinucleotide='GA', location=24),
        DinucleotideLocation(dinucleotide='GT', location=24),
        DinucleotideLocation(dinucleotide='TC', location=24),
    )

    CLASSIFICATION_DINUCLEOTIDES_OF_INTEREST = (
        DinucleotideLocation(dinucleotide='CG', location=11),
        DinucleotideLocation(dinucleotide='GA', location=15),
        DinucleotideLocation(dinucleotide='TT', location=16),
        DinucleotideLocation(dinucleotide='CC', location=20),
        DinucleotideLocation(dinucleotide='TA', location=22),
        DinucleotideLocation(dinucleotide='CG', location=23),
        DinucleotideLocation(dinucleotide='TC', location=23),
        DinucleotideLocation(dinucleotide='TG', location=23),
        DinucleotideLocation(dinucleotide='CC', location=24),
        DinucleotideLocation(dinucleotide='GA', location=24),
        DinucleotideLocation(dinucleotide='GC', location=24),
        DinucleotideLocation(dinucleotide='GT', location=24),
        DinucleotideLocation(dinucleotide='TC', location=24),
    )

    CLASSIFICATION_DINUCLEOTIDES = [
        'AA',
        'AC',
        'AG',
        'AT',
        'CA',
        'CC',
        'CG',
        'CT',
        'GA',
        'GC',
        'GG',
        'GT',
        'TA',
        'TC',
        'TG',
        'TT',
    ]

    REGRESSION_DINUCLEOTIDES = [
        'CA',
        'CT',
        'GC',
        'TC',
        'TG',
        'TT',
    ]


    #determines gc content of given sequence
    def gc(self, seq, features, index):
        features[index] = round((seq.count('C') + seq.count('G'))/float(len(seq)) * 100, 2)

    #counts appearance of dinucleotides in sequence
    def di_content(self, seq, dinucleotides_to_count, features, start_index):
        for idx, dinucleotide in enumerate(dinucleotides_to_count):
            count = start = 0
            while True:
                start = seq.find(dinucleotide, start) + 1
                if start:
                    count += 1
                else:
                    features[start_index+idx] = count
                    break

    #checks if specific PAM is present in sequence
    def pam(self, seq, features, index):
        if seq[24:28] == 'TGGT':
            features[index] = 1

    #checks if given position-specific nucleotides are present in sequence
    def nucleotide(self, seq, nucleotides_of_interest, features, start_index):
        for idx, nucleotide_loc in enumerate(nucleotides_of_interest):
            if seq[nucleotide_loc.location-1] == nucleotide_loc.nucleotide:
                features[start_index+idx] = 1

    #checks if given position-specific dinucleotides are present in sequence
    def dinucleotide(self, seq, dinucleotides_of_interest, features, start_index):
        #-1 is since a sequence of length N has N-1 dinucleotides
        for idx, dinucleotides_loc in enumerate(dinucleotides_of_interest):
            location = dinucleotides_loc.location
            if seq[location-1:location+1] == dinucleotides_loc.dinucleotide:
                features[start_index+idx] = 1

    #generates a feature vector from a given 30 nucleotide sequence
    def getFeatures(self, seq):
        if self.is_regression:
            features = [0] * 63
            self.gc(seq, features, 0)
            features[1] = seq.count('A')
            features[2] = seq.count('C')
            features[3] = seq.count('G')
            features[4] = seq.count('T')
            self.di_content(seq, self.REGRESSION_DINUCLEOTIDES, features, 5)
            self.nucleotide(seq, self.REGRESSION_NUCLEOTIDES_OF_INTEREST, features, 11)
            self.dinucleotide(seq, self.REGRESSION_DINUCLEOTIDES_OF_INTEREST, features, 24)
            self.pam(seq, features, 62)
        else:
            features = [0] * 46
            self.gc(seq, features, 0)
            features[1] = seq.count('A')
            features[2] = seq.count('C')
            features[3] = seq.count('G')
            features[4] = seq.count('T')
            self.di_content(seq, self.CLASSIFICATION_DINUCLEOTIDES, features, 5)
            self.nucleotide(seq, self.CLASSIFICATION_NUCLEOTIDES_OF_INTEREST, features, 21)
            self.dinucleotide(seq, self.CLASSIFICATION_DINUCLEOTIDES_OF_INTEREST, features, 33)
        return features

    ##############################################################################################
    ## METHODS NEEDED FOR FITTING THE TOOL DATA INTERFACE
    ## This code is adapted from the original Tuscan code.
    ## Where possible pre-trained models have been saved in pickle/joblib files
    ##############################################################################################

    #The training set is saved in a pickle file
    def loadTrainingSet(self):
        #There are different training sets for regression and classification
        if self.is_regression:
            f_name = './tuscan-model/training-set-tuscan-regression'
        else:
            f_name = './tuscan-model/training-set-tuscan-classification'

        #load the training set
        infile = open(f_name,'rb')
        train = pickle.load(infile)
        train_df = pd.DataFrame(np.array(train))
        infile.close()

        return train_df

    #The feature names have been created based on the original tuscan code and split in categories
    def loadFeatureNames(self):
        feature_names = []
        if self.is_regression: #The features for the regression model
            feature_names = [''] * 63
            #arrays to be used for regression features
            dinucs = self.REGRESSION_DINUCLEOTIDES
            nuc_of_interest = self.REGRESSION_NUCLEOTIDES_OF_INTEREST
            dinuc_of_interest = self.REGRESSION_DINUCLEOTIDES_OF_INTEREST

        else: #Features for the classification model
            feature_names = [''] * 46
            #arrays to be used for classification features
            dinucs = self.CLASSIFICATION_DINUCLEOTIDES
            nuc_of_interest = self.CLASSIFICATION_NUCLEOTIDES_OF_INTEREST
            dinuc_of_interest = self.CLASSIFICATION_DINUCLEOTIDES_OF_INTEREST

        feature_names[0] = "gc" #Guanine and Cythosine content

        #nucleotide counts
        feature_names[1] = "#A"
        feature_names[2] = "#C"
        feature_names[3] = "#G"
        feature_names[4] = "#T"

        f_pos = 5
        #dinucleotide content
        for dinuc in dinucs:
            feature_names[f_pos] = "#" + dinuc
            f_pos = f_pos + 1

        #nucleotides at a specific position
        for nuc in nuc_of_interest:
            feature_names[f_pos] = nuc.nucleotide + ":" + str(nuc.location - 5) #-4 downstream nucleotides, starting from 1
            f_pos = f_pos + 1

        #dinucleotides at a specific position
        for dinuc in dinuc_of_interest:
            feature_names[f_pos] = dinuc.dinucleotide + ":" + str(dinuc.location - 5) #-4 downstream nucleotides, starting from 1
            f_pos = f_pos + 1

        if self.is_regression:
            #If there is TGGT in the PAM
            feature_names[f_pos] = "TGGT:PAM"

        return feature_names


    #loads the regression/classification model from joblib library
    def loadModel(self):
        # Load the appropriate model
        if self.is_regression:
            rfm = './tuscan-model/rfModelregressor.joblib'
            with open(rfm, 'rb') as f:
                rf = joblib.load(f)
        else:
            rfm = './tuscan-model/rfModelclassifier.joblib'
            with open(rfm, 'rb') as f:
                rf = joblib.load(f)
        return rf
