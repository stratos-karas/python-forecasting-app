#!/usr/bin/env python3

import PySimpleGUI as gui
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import libForecast as libf
import yfinance
import numpy as np
from datetime import datetime


###########################################################################################
###########################################################################################
###########################################################################################

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


###########################################################################################
###########################################################################################
###########################################################################################

# Init

tickers_NASDAQ = pd.read_csv('Tickers_NASDAQ.csv')[['Symbol', 'Name']]
symbol_name_NASDAQ = (tickers_NASDAQ['Symbol'] + ', ' + tickers_NASDAQ['Name']).tolist()
methods = ['LRL', 'Theta', 'Damped', 'Holt', 'Arima', 'Exponential', 'All']

# Theme

gui.theme('Dark Blue 3')  

# Layout

layout_left = [
    [gui.Text('Choose ticker of share')],
    [gui.InputCombo(symbol_name_NASDAQ, size=(50, 7), expand_x=True, enable_events=True, key='_SHARE_')],
    
    [gui.Text('Select historical data', size=(26, 0), expand_x=True), 
        gui.Text("Forecast's horizon", size=(24, 0), expand_x=True)],
    [gui.InputCombo(['1mo', '3mo', '6mo', '1y'], default_value='6mo', size=(25, 2), expand_x=True, enable_events=True, key='_HISTORY_'), 
        gui.Input(size=(25, 3), expand_x=True, enable_events=True, key='_HORIZON_', 
            tooltip="Horizon is the days ahead you want a model to predict")],

    [
        gui.Frame('Forecasting methods',
        [
            [gui.Checkbox(name, enable_events=True, key=name) for name in methods[:5]],
            [gui.Checkbox(name, enable_events=True, key=name) for name in methods[5:8]],
        ], expand_x=True
        )
    ],

    [
        gui.Frame('Forecasting and Plotting Options',
        [
            [gui.Checkbox('Enable Confidence Intervals', key='_CI_')],
            [gui.Checkbox('Compute Fibonacci Retracements', key='_FIBONACCI_')]
        ], expand_x=True
        )
    ],

    [gui.Button('Produce Graph', size=(25, 2), key='_PRODUCE_GRAPH_'), gui.Button('Save Graph', size=(25, 2), key='_SAVE_GRAPH_')]
]

layout_right = [
    [
        gui.Frame('Zoom (%)', 
        [
            [gui.Slider(range=(0, 100), orientation='h', size=(76, 10), resolution=1, default_value=0, tick_interval=0, key='_ZOOM_', enable_events=True)]
        ], expand_x=True
        )
    ],

    [gui.Canvas(key='_FIGURE_')]
]

layout = [
    [gui.Column(layout_left), gui.VerticalSeparator(), gui.Column(layout_right)]
]

# Window

window = gui.Window('Statistical Forecasting', layout, location=(400, 400), finalize=True)
window.refresh()

# Events

# Plot a placeholder for the forecasts
fig = libf.dummy_plot()
latest_fig = draw_figure(window['_FIGURE_'].TKCanvas, fig)

while True:
    
    event, values = window.read()

    if event == '_PRODUCE_GRAPH_':

        share_name = values['_SHARE_'].split(',')[0]
        history = values['_HISTORY_']
        horizon = int(values['_HORIZON_']) if values['_HORIZON_'] != '' else 1
        confidence_interval = values['_CI_']
        zoom = values['_ZOOM_']
        fibonacci_enabled = values['_FIBONACCI_']
        
        forecasting_methods = []
        for method in methods:
            if values[method] == True and method != 'All':
                forecasting_methods.append(method.lower())

        df = yfinance.Ticker(share_name).history(history)
        data = np.array( df['Close'] )
        forecasts = libf.forecasts(data, forecasting_methods, 7, horizon)

        if latest_fig != None:
            plt.clf()
            latest_fig.get_tk_widget().forget()
        
        fig = libf.produce_plot_and_stats(data, df.index, forecasting_methods, forecasts, confidence_interval, zoom, fibonacci_enabled)
        latest_fig = draw_figure(window['_FIGURE_'].TKCanvas, fig)

    elif event == '_SAVE_GRAPH_':
        if latest_fig != None:
            plt.savefig(str(datetime.now()) + '.png')

    elif event in methods:
        if event == 'All':
            for method in methods:
                window[method].update(value=True)
        else:
            if window['All'].get() == True:
                window[method].update(value=False)

    elif event in (gui.WIN_CLOSED, 'Exit'):
        break

window.close()
