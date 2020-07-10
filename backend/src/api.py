import flask
from flask import request
from plotPositionsFromPickle import plotPosForFile
from plotShapFromPickle import plotShapForFile

import io
from flask import Response
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask_cors import CORS, cross_origin

import shap
import base64

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def home():
    return "Backend Running"


@app.route('/shap', methods=['GET'])
@cross_origin(origins="*")
def shapf():
    toolName = request.args.get('tool')
    data = request.args.get('data')


    fileName = "SHAP-" + toolName + "-" + data

    shap_values, dataset = plotShapForFile(fileName)
    fig = shap.summary_plot(shap_values, dataset)
    pic_IObytes = io.BytesIO()
    plt.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read())
    plt.close()

    return pic_hash

@app.route('/pos', methods=['GET'])
@cross_origin(origins="*")
def pos():
    toolName = request.args.get('tool')
    data = request.args.get('data')


    fileName = "SHAP-" + toolName + "-" + data

    plt = plotPosForFile(fileName)

    pic_IObytes = io.BytesIO()
    plt.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read())
    plt.close()
    return pic_hash

app.run()
