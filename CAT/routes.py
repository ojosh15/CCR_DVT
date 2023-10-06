from flask import render_template, url_for, request, flash, redirect
from CAT import app
import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px
from CCR.ccr import ccr
import glob
import re
import sys

from CAT import app, db
from CAT.forms import analysisConfigurationForm, settingsForm, componentForm
from CAT.models import Component


@app.route('/')
@app.route('/analyze')
def analyze():
    analysis_form = analysisConfigurationForm()
    settings_form = settingsForm()

    l = 1001
    N = np.linspace(0,1000,l,dtype=int)
    freq = N
    mag = np.random.rand(l)

    freq1 = N
    mag1 = np.random.rand(l)
    
    item = np.full(shape=l,fill_value=1,dtype=np.int)
    item1 = np.full(shape=l,fill_value=2,dtype=np.int)

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=item, y=freq, z=mag, mode='lines', line = dict(color='yellow', width=2)))
    fig.add_trace(go.Scatter3d(x=item1, y=freq1, z=mag1, mode='lines', line = dict(color='red', width=2)))

    fig.update_layout(scene=dict(xaxis=dict(title=dict(text="Items",font=dict(color="white",size=16)),mirror=True,ticks="outside",showline=True,zeroline=False,backgroundcolor='black',color='lightgrey'),
                                 yaxis=dict(title=dict(text="Frequency (MHz)",font=dict(color="white",size=16)),mirror=True,ticks="outside",showline=True,zeroline=False,backgroundcolor='black',color='lightgrey'),
                                 zaxis=dict(title=dict(text="Power (dBm)",font=dict(color="white",size=16)),mirror=True,ticks="outside",showline=True,zeroline=False,backgroundcolor='black',color='lightgrey'),
                                 camera_eye_z=0.75),
                      autosize=True,
                    plot_bgcolor="black",
                    paper_bgcolor="#363535",
                    title=dict(text="Power Vs. Frequency",x=0.5,xanchor="center",yanchor="top",font=dict(color="white",size=24)),
                    font_family="Arial",
                    margin=dict(l=10, r=10, t=10, b=10),
                    legend=dict(yanchor="top",y=0.9,xanchor="right",x=0.99,bgcolor="rgba(0,0,0,0)",font=dict(color="white",size=14)),
                    modebar=dict(add=["togglespikelines","hovercompare","v1hovermode"]),
                    hovermode="closest",
                    hoverlabel=dict(font=dict(color="white",size=12),bgcolor="#363535"))
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    #fig.update_xaxes(title=dict(text="Items",font=dict(color="white",size=16)),mirror=True,ticks="outside",showline=True,zeroline=False,color="white")
    #fig.update_yaxes(title=dict(text="Frequency (MHz)",font=dict(color="white",size=16)),mirror=True,ticks="outside",showline=True,zeroline=False,color="white")
    #fig.update_zaxes(title=dict(text="Power (dBm)",font=dict(color="white",size=16)),mirror=True,ticks="outside",showline=True,zeroline=False,color="white")

    graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('analyze.html',title='Analyze',graphJson=graphJson,analysis_form=analysis_form,settings_form=settings_form)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...' 

@app.route('/database', methods=['GET','POST'])
def database():
    settings_form = settingsForm()
    form = componentForm()
    if form.validate_on_submit():
        comp = Component(model=form.model.data,comp_type=form.comp_type.data,manufacturer=form.manufacturer.data,active=form.active.data,
                         source=form.source.data)
        comp.save()
        flash('Component has been saved successfully!', 'success')
        return redirect(url_for('database'))
        
    return render_template('database.html',title='Database',form=form,settings_form=settings_form)