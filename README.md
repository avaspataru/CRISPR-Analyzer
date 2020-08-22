# CRISPR-Analyzer
A web application which helps us investigate the importance of features in ML-based tools for CRISPR/Cas9 gRNA efficiency prediction. 

## What it does
The application has a number of models and datasets previously loaded. For each model and dataset pair (upon user selection), it can calculate the SHAP values of each feature. The SHAP values are a great way of measuring feature importance across models (see [link](https://towardsdatascience.com/explain-your-model-with-the-shap-values-bc36aac4de3d)). The SHAP values are then used to generate various plots:
  * SHAP summary plot - showing the top 20 most important features by average SHAP value across the dataset, with the SHAP value on each point. 
  * Positional plot - showing the position-specific nucleotide preference of the model. The values here are average SHAP values across the data points which have the specifc nucleotide at the position of interest. 
  
Or to compare two or more models on either or both datasets. This is done by generating a positional plot which has information from all the selected models. 

