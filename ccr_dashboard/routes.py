from flask import render_template, url_for
from ccr_dashboard import app
import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px

@app.route('/')
def index():
    N = 40
    x1 = np.linspace(0, 1, N)
    y1 = np.random.randn(N)
    df1 = pd.DataFrame({'Frequency': x1, 'Magnitude': y1})
    
    x2 = np.linspace(0, 1, N)
    y2 = np.random.randn(N)
    df2 = pd.DataFrame({'Frequency': x2, 'Magnitude': y2})

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1['Frequency'], y=df1['Magnitude'], line = dict(color='yellow', width=2)))
    fig.add_trace(go.Scatter(x=df2['Frequency'], y=df2['Magnitude'], line = dict(color='red', width=2)))

    fig.update_layout(plot_bgcolor="black",
                   paper_bgcolor="#363535",
                   height=800,
                   title=dict(text="Power Vs. Frequency",x=0.5,xanchor="center",yanchor="top",font=dict(color="white",size=24)),
                   font_family="Arial",
                   margin=dict(l=20,r=20,t=50,b=20),
                   legend=dict(yanchor="top",y=0.99,xanchor="right",x=0.99,bgcolor="rgba(0,0,0,0)",font=dict(color="white",size=14)),
                   modebar=dict(add=["togglespikelines","hovercompare","v1hovermode"]),
                   hovermode="x unified")
    fig.update_xaxes(title=dict(text="Frequency (MHz)",font=dict(color="white",size=16)),mirror=True,ticks="outside",showline=True,zeroline=False,color="white")
    fig.update_yaxes(title=dict(text="Power (dBm)",font=dict(color="white",size=16)),mirror=True,ticks="outside",showline=True,zeroline=False,color="white")

    graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    ccr_sns = np.linspace(1,80,80,dtype=int)

    return render_template('layout.html',title='Dashboard',graphJson=graphJson,ccr_sns=ccr_sns)