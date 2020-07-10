from utils import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#all of the tools to be compared, including scoring methods and model types (tuscan, chop-chop)
tools = ['ssc' ,'tuscan-classification', 'tuscan-regression', 'sgrnascorer2','wu-crispr','chop-chop-xu','chop-chop-doench','chop-chop-moreno']

#the datasets these tools were ran on
datasets = ['xu', 'doench']

#the feature names to be printed
features = []
for p in range(0,20):
    for n in nucleotides:
        features.append(str(p) + n)

#fill in data (the average shap values for each fetaure for each tool)
methods = []
table = []
for tool in tools:
    for data in datasets:
        print("For " + tool + " on " + data)
        pickleFileName = "SHAP-" + tool + "-" + data
        methodName = getShorthand(tool) + '-' + data

        #get a list of tuples (avg shap val, feature name)
        featureImp = getAvgShapValues(pickleFileName)

        #creates dictionary where average[nucleotide id][position] = the average shap value of the nucleotide being at that position
        averages = getShapValsForPosFeatures(featureImp) #function def in utils

        #create data in order 0A,0C,0G,0T,1A,1C.....19T
        data = []
        for p in range(0,20):
            for n in range(0,4):
                data.append(averages[n][p])

        #append for csv
        methods.append(methodName)
        table.append(np.array(data))

#arrange data table
table = np.array(table)

#save csv
df = pd.DataFrame(data=table, columns=features, index=methods)
df.to_csv('../results/avg_shap_vals.csv')

#plot
fig, ax = plt.subplots(figsize=(16,80))
sns.heatmap(df, center=0)
ax.set_title("Average Shap Values Across Methods")
plt.yticks(rotation=0)
plt.xticks(range(0,len(features)),features)

#save and show plot
plt.savefig("../plots/compare-guide-positions/all-heatmap.png")
plt.show()
