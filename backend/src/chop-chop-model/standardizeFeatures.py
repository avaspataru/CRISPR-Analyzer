
"""
A script which modifies the scoring methods to standardize the feature names.

CHOP-CHOP counts the positions in the guide from the PAM towards the start of
the guide (20 - 1) and the positions after the PAM in increasing order.

All the other tools analysed in this project count the guide positions in
increasing order. Therefore, to standardize, this script changes the scoring
method dictionaries from below to count the guide positions increasingly.

"""


######################################################################
## Coefficients for the 3 scoring methods extracted from the original
## CHOP CHOP source code.
## see: https://bitbucket.org/valenlab/chopchop/src/master/
######################################################################
XU_2015 = {'C18':-0.113781378,
           'G17':0.080289971,
           'A16':0.025840846,'G16':0.072680697,
           'G15':0.100642827,
           'G14':0.082839514,
           'T14':-0.070933894,
           'A12':0.02156311,
           'A11':0.129118902,
           'A10':0.030483786,'T10':-0.169986128,
           'A9':0.093646913,
           'G7':-0.214271553,'T7':0.073750154,
           'A6':0.202820147,
           'A5':0.129158071,
           'G4':0.107523301,'T4':-0.349240474,
           'C3':0.23502822,'T3':-0.145493093,
           'G2':0.238517854,'T2':-0.300975354,
           'C1':-0.125927965,'G1':0.353047311,'T1':-0.221752041,
           'PAMT1':-0.155910373,
           '1C':0.179639101,
           '4T':-0.116646129}

DOENCH_2014 = {"Intercept": 0.5976361543,
               "G23": -0.2753771278,"TG22": -0.625778696,
               "A22": -0.3238874564,"C22": 0.1721288713,
               "C21": -0.1006662089,
               "C20": -0.20180294,"G20": 0.2459566331,"CG19": 0.3000433167,
               "C19": 0.0983768352,"A19": 0.0364400412,"AA18":-0.8348362447,"AT18": 0.7606277721,
               "C18":-0.7411812913,"G18":-0.3932643973,"GG17":-0.4908167494,
               "A13":-0.4660990147,"GG12":-1.5169074394,"AT12": 0.7092612002,"CT12": 0.4962986088,"TT12":-0.5868738941,
               "GG11":-0.3345637351,
               "AG10": 0.7638499303,"CG10":-0.5370251697,
               "A10": 0.0853769455,"C10":-0.0138139718,
               "A9": 0.2726205124,"C9": -0.119022648,"T9":-0.2859442224,
               "A8": 0.0974545916,"G8":-0.1755461698,"GT7":-0.7981461328,
               "C7":-0.3457954508,"G7":-0.6780964263,
               "A6": 0.2250890296,"C6":-0.5077940514,"GG5":-0.6668087295,"CT5": 0.3531832525,
               "G5":-0.4173735974,"T5":-0.0543069593,"CC4": 0.7480720923,"GT4":-0.3672667722,
               "G4": 0.379899366,"T4":-0.0907126437,"CA3": 0.5682091316,"GC3": 0.3290720742,"AG3":-0.8364567552,"GG3":-0.7822075841,
               "C3": 0.0578233185,"T3":-0.5305672958,"CT2":-1.0296929571,
               "T2":-0.8770074285,"GC1": 0.8561978226,"TC1":-0.4632076791,
               "C1":-0.8762358461,"G1": 0.2789162593,"T1":-0.4031022177,"AA0":-0.5794923887,"GA0": 0.6490755373,
               "PAMC1": 0.287935617,"PAMA1":-0.0773007042,"PAMT1":-0.2216372166, "PAMAG1":-0.0773007042,"PAMCG1":  0.287935617,"PAMTG1":-0.2216372166,
               "1G":-0.6890166818,"1T": 0.1178775773,
               "2C":-0.1604453039,"2GG":-0.6977400239,
               "3G": 0.3863425849,
               "gc_low":-0.2026258943,
               "gc_high": -0.166587752}

MORENO_MATEOS_2015 = {"Intercept": 0.1839309436,
                      "G26":-0.0296937089,
                      "CG23":0.0246817853,"GT23":0.0229499956,
                      "G23":-0.0054488693,"A23":-0.0421535206,
                      "C18":0.0024492239,"G18":0.1146006812,"GG17":-0.0015779899,"CG17":0.0541714023,
                      "G17":0.0677391822,"GA16":0.0637170933,"GG16":0.0268021579,"AA16":-0.0169054146,
                      "A16":-0.0182872921,"G16":0.0209290394,"TG15":0.0536784362,
                      "A15":0.0116332345,"G15":0.0275911379,"GG14":0.0418830086,
                      "A14":0.0176289243,"T14":0.0354451707,"C14":0.069495944,"G14":0.0613609047,"GG13":0.0743558476,"TT13":-0.0861877104,
                      "G13":0.0251167144,"A13":-0.0184872292,
                      "A12":-0.0105952955,"C12":-0.0004777273,"G12":0.0511297167,"GT11":0.0533728222,
                      "G11":0.0379709424,"C11":-0.0216386089,
                      "G10":0.0154937801,"TT9":0.0349288099,
                      "A9":-0.033820432,"G9":0.0164578159,"GT8":0.0459089908,"TG8":0.0023917441,"TT8":-0.094424075,
                      "A8":-0.0155764989,"G8":0.0179168437,"AA7":-0.0973770966,
                      "C7":0.0150895135,"AG6":0.0097407989,
                      "T6":-0.0687304967,"C6":0.0342629207,"CC5":0.0889196009,
                      "T5":0.0132240349,"G5":0.1011443803,"C5":0.0376316197,"A5":0.0319309088,
                      "T4":-0.0014222433,"CC3":0.0950722865,"TG3":0.1067185626,"GA3":-0.0543384557,"GT3":-0.0663880754,
                      "T3":-0.0119961724,"A3":0.0374664775,"C3":0.0529723137,"G3":0.1054883249,"AC2":0.0622193698,"TG2":0.0609521143,
                      "C2":-0.031648353,"A2":0.010506405,"GG1":0.1115594407,"CG1":-0.0734536087,
                      "G1":0.0361466487,"C1":-0.0003689729,"TC0":-0.0842648932,
                      "PAMT1":-0.0002808449,"PAMA1":0.0191268154,"PAMC1":0.0799339215,"PAMG1":0.0851510516,
                      "1G":-0.0463159143,"1C":-0.0131827326,"1T":0.0172631618,"1CA":0.0577598507,
                      "2C":-0.0307155561,"2A":0.0015897498,"2TG":0.0481368123,"2GT":0.0734253504,"2GA":-0.01227989,
                      "3G":0.0307124897,
                      "5G":-0.0141671226,"5T":-0.0176476917,"5GA":-0.0377977074,"5AG":-0.0419359085,
                      "6A":0.0485962592}

######################################################################
## Code which creates three other dictionaries with standardized
## feature names.
######################################################################

# from  20 19 18 17 16 15 14 13 12 11 10 9  8  7  6  5  4  3  2  1
# to    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19
def revert(pos):
    return 20-pos

# take a scoring dictionary and return one with the feature names changed
def standardize(scoreDict):
    newScoreDict = {}
    for feature in scoreDict:
        value = scoreDict[feature]

        if feature in ["Intercept","gc_low","gc_high"]: #should be left with the same name
            newScoreDict[feature] = value
            continue

        if feature[0:3] == "PAM": #Pam positions are counted 1,2,3 and should be 0,1,2
            if feature[4].isnumeric(): #PAMNi
                nuc = feature[3]
                pos = int(feature[4]) #only (1,2,3)

            else: #PAMNNi
                nuc = feature[3:5]
                pos = int(feature[5]) #only (1,2,3)

            newPos = pos - 1
            newFeature = "PAM" + nuc + str(newPos)
            newScoreDict[newFeature] = value
            continue

        if feature[0].isnumeric(): #Feature names that start with a number are in the tail
            #the positions are (1,2,3,4,5,6) and should be (0,1,2,3,4,5)
            newPos = int(feature[0]) - 1
            newFeature = str(newPos) + feature[1:]
            newScoreDict[newFeature] = value
            continue

        #feature name is NNi or Ni
        if feature[1].isnumeric(): #Ni
            nuc = feature[0]
            position = int(feature[1:])
        else: #NNi
            nuc = feature[0:2]
            position = int(feature[2:])

        newPosition = revert(position)
        newFeature = nuc+str(newPosition)
        newScoreDict[newFeature] = value

    return newScoreDict

def getXuScoring():
    return standardize(XU_2015)

def getDoenchScoring():
    return standardize(DOENCH_2014)

def getMorenoScoring():
    return standardize(MORENO_MATEOS_2015)
