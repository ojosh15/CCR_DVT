from flask import render_template, url_for
from ccr_dashboard import app
import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px
from CCR.ccr import ccr
import pandas as pd
import glob
import re

from ccr_dashboard.forms import analysisConfigurationForm, settingsForm



@app.route('/')
@app.route('/dashboard')
def analyze():
    analysis_form = analysisConfigurationForm()
    settings_form = settingsForm()
    unit14 = ccr(14,'LA')
    target_dir = r'C:\\Users\\joshua.outhous\\Documents\\CCR\\Unit 14\\Main\\'
    ccr_unit = 'main'
    p1 = re.compile(r'J\d+_')
    p2 = re.compile(r'_J\d+')
    for file_name in glob.glob(target_dir+'*.csv'):
        m1 = p1.search(file_name)
        m2 = p2.search(file_name)
        inputJack = m1.group()[:-1]
        outputJack = m2.group()[1:]
        df = pd.read_csv(file_name)
        data = [df.iloc[:,0],df.iloc[:,1]]
        unit14.add_data(ccr_unit,inputJack,outputJack,data)
    freq = unit14.mainUnit['J2_J4']['Oct 2022'][0]
    mag = unit14.mainUnit['J2_J4']['Oct 2022'][1]
    
    freq1 = unit14.mainUnit['J2_J5']['Oct 2022'][0]
    mag1 = unit14.mainUnit['J2_J5']['Oct 2022'][1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=freq, y=mag, line = dict(color='yellow', width=2)))
    fig.add_trace(go.Scatter(x=freq1, y=mag1, line = dict(color='red', width=2)))

    fig.update_layout(plot_bgcolor="black",
                   paper_bgcolor="#363535",
                   height=800,
                   title=dict(text="Power Vs. Frequency",x=0.5,xanchor="center",yanchor="top",font=dict(color="white",size=24)),
                   font_family="Arial",
                   margin=dict(l=20,r=20,t=50,b=20),
                   legend=dict(yanchor="top",y=0.99,xanchor="right",x=0.99,bgcolor="rgba(0,0,0,0)",font=dict(color="white",size=14)),
                   modebar=dict(add=["togglespikelines","hovercompare","v1hovermode"]),
                   hovermode="closest",
                   hoverlabel=dict(font=dict(color="white",size=12),bgcolor="#363535"))
    fig.update_xaxes(title=dict(text="Frequency (MHz)",font=dict(color="white",size=16)),mirror=True,ticks="outside",showline=True,zeroline=False,color="white")
    fig.update_yaxes(title=dict(text="Power (dBm)",font=dict(color="white",size=16)),mirror=True,ticks="outside",showline=True,zeroline=False,color="white")

    graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layout.html',title='Dashboard',graphJson=graphJson,analysis_form=analysis_form,settings_form=settings_form)