import pickle
import argparse
import shap

#get the pickle file from arguments
parser = argparse.ArgumentParser(description="specify the file to unpicke for the SHAP values")
parser.add_argument('--file', help='path to pickle file', required=True)
args = parser.parse_args()

fileName = args.file

#load the SHAP values and the data
p = open('../results/'+fileName,"rb")
print("Loading data...")
shap_values = pickle.load(p)
dataset = pickle.load(p)
p.close()

#plot
print("Plotting...")
shap.summary_plot(shap_values, dataset)
