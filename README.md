![Logo](https://github.com/avaspataru/CRISPR-Analyzer/blob/master/screens/logo.png)

A web application which helps us investigate the importance of features in ML-based tools for CRISPR/Cas9 gRNA efficiency prediction. This was developed as part of an MSc project in 2020.  

## What it does
The application has a number of models and datasets previously loaded. For each model and dataset pair (upon user selection), it can calculate the SHAP values of each feature. The SHAP values are a great way of measuring feature importance across models (see [link](https://towardsdatascience.com/explain-your-model-with-the-shap-values-bc36aac4de3d)).

The SHAP values are then used to generate various plots:
  * SHAP summary plot - showing the top 20 most important features by average SHAP value across the dataset, with the SHAP value on each point. 
  * Positional plot - showing the position-specific nucleotide preference of the model. The values here are average SHAP values across the data points which have the specifc nucleotide at the position of interest. 
  
Or to compare two or more models on either or both datasets. This is done by generating a positional plot which has information from all the selected models. 

## Who can use it
This application can be used by anyone with an interest in efficiency prediction tools forCRISPR. The users can either use the tool to contrast their own model with models loaded inthe application or to chose which model to use based on the analysis. A biologist with good knowledge of CRISPR efficiency factors may wish to still use a model,  but be undecided which.   Having  a  tool  which  can  easily  check  a  range  of  existing  models  an ddisplay the basis of how these models rank efficiency, can help the scientist decide which of the models to trust.  

Another great aspect of having this tool is the fact that it providespreviously unknown insight into the efficiency factors of CRISPR gRNA. There are a range of papers published with some information about the models, however there is no way to contrast these, as each researcher used their own method for interpreting model predictions.

## How it works 
The application combines a python backend with a react frontend, which communicate via REST APIs. The frontend sends requests based on what plot the user is waiting for and the backend computes the plot and sends back a base64 representation of it, which the frontend decodes and displays. 

To ensure that the application runs in a timely manner, once the SHAP values have been calculated for a model-dataset pair, they are saved in a pickle file. Whenever the analysis is ran again, the SHAP values will be taken from the pickle file instead of recalculation. 

![Sequence_diagram](https://github.com/avaspataru/CRISPR-Analyzer/blob/master/screens/use_case.jpg)

## Installation instructions 
The application is made up of a backend (backend folder) and a frontend (frontend folder). It requires Python3 for the backend and React with npm for the frontend. 


To run the python backend (after installing packages): 
```
cd ./backend/src/
python api.py
```

To run the react frontend (after installing packages):
```
cd ./webapp
npm start
```

For the communication between the two to work, the backend should run on port 5000 and the frontend on 3000. 

## Work in progress
* allowing the user to upload their own model 
* allowing the user to publish their model and have it available for everyone (after review)
* allowing the user to use customized datasets 
* adding an instructions page 
* adding radial plots for comparison of positional-specific nucleotide preference
* fix namings on plots (especially positional compare)

## Screens 
The design combines simple bootstrap components for a minimalist design, making it very simple and intuitive for the user to know what to access. The application also accounts for any possible user misjudgements (e.g. running the analysis on no datasets).

### Start screen 
![Image of start screen](https://github.com/avaspataru/CRISPR-Analyzer/blob/master/screens/Start_screen.JPG)

### SHAP summary plot screen
![Image of SHAP screen](https://github.com/avaspataru/CRISPR-Analyzer/blob/master/screens/Shap_screen.JPG)

### Compare models screen
![Image of compare screen](https://github.com/avaspataru/CRISPR-Analyzer/blob/master/screens/Compare_screen.JPG)


