from fastapi import FastAPI
from typing import Union
from models.STP import STP
import matplotlib.pyplot as plt
import numpy as np
from utils.eq_function import fxn
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from sympy import Symbol, solve, Eq
import io
import base64

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/graph/")
async def graph(data: STP):       
    q_values = np.array(list(dict(data.QuaterLevel).values()))
    s_values = np.array(list(dict(data.StaticLevel).values()))
    
    # Plotting the graph
    plt.scatter(q_values, s_values)
    plt.xlabel("Q(L/min)")
    plt.ylabel("s(m)")
    
    # Plotting The TrendLine
    popt, popc = curve_fit(fxn, q_values, s_values)
    s_hat = fxn(q_values, *popt)
    plt.plot(q_values, s_hat, "r--", lw=1)
    text = f"$y={popt[0]:0.4f}\;x^2{popt[1]:+0.4f}\;x$\n$R^2 = {r2_score(s_values, s_hat):0.3f}$"
    plt.gca().text(0.05, 0.95, text, transform=plt.gca().transAxes, fontsize=14, verticalalignment='top')
    plt.grid()
    
    #convert the plot to a byte io 
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    
    buffer.seek(0)
    
    plt.clf()
    
    # get the econded image
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    # calculate for S_max which will be needed for the equation
    s_max = data.pump_setting - data.buffer_ - data.static_water_level
    
    #Calculating for Qm using the symbols module
    Qm = Symbol("Qm")
    equation = Eq(float(s_max), popt[0] * Qm ** 2 + popt[1] * Qm)
    roots = solve(equation, Qm)
    positive_roots = roots[1]
    
    q = round(positive_roots, 2)
    qm = positive_roots * 1.44
    
    response = {
        "image": encoded_image,
        "q": str(q),
        "qm": str(qm)
    }
    
    return response
        