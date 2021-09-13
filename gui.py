from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget,\
     QVBoxLayout, QGridLayout, QGroupBox, QComboBox, QSpinBox, QLabel, QCheckBox, QPushButton

import graphs
import yfinance
import libForecast as libf
import numpy as np
import pandas as pd

app = QApplication([])
app.setApplicationDisplayName("Forecasts for the poor")
app.setApplicationName("Forecasts for the poor")

tabs = QTabWidget()
# tabs.setStyleSheet("QTabWidget { color: white; background-color:  }")
tabs.setStyleSheet(
    " QTabWidget { background-color: #00091a } "
    " QTabBar { color:white; background-color: #00091a } "
    " QPushButton {color: white; background-color: #24478f} "
    " QGroupBox {color: white; background-color: #24478f; border-radius: 5px} "
    " QLabel {color: white} "
    " QCheckBox {color: white} "
    " QGraphicsWidget { background-color: #00091a }"
    )

################ TAB TOOLS ###############

tab_tools = QWidget()
layout_tools = QVBoxLayout()

gbox_tickers = QGroupBox('Tickers')
gbox_methods = QGroupBox('Forecasting Methods')
gbox_indicators = QGroupBox('Forecasting Indicators')

################# Tickers Group #######################

layout_tools.addWidget(gbox_tickers)

layout_tickers = QVBoxLayout()

input_tickers = QComboBox()
input_tickers.setEditable(True)
input_tickers.setDuplicatesEnabled(False)

tickers_NASDAQ = pd.read_csv('Tickers_NASDAQ.csv')[['Symbol', 'Name']]
symbol_name_NASDAQ = (tickers_NASDAQ['Symbol'] + ', ' + tickers_NASDAQ['Name']).tolist()
input_tickers.insertItems(0, symbol_name_NASDAQ)

layout_history_horizon = QGridLayout()

input_history = QComboBox()
input_history.setEditable(False)
input_history.insertItems(0, ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'max'])

input_interval = QComboBox()
input_interval.setEditable(False)
input_interval.insertItems(0, ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'])

input_horizon = QSpinBox()

layout_history_horizon.addWidget(QLabel('Period'), 0, 0)
layout_history_horizon.addWidget(input_history, 1, 0)
layout_history_horizon.addWidget(QLabel('Interval'), 0, 1)
layout_history_horizon.addWidget(input_interval, 1, 1)
layout_history_horizon.addWidget(QLabel("Horizon"), 0, 2)
layout_history_horizon.addWidget(input_horizon, 1, 2)

layout_tickers.addWidget(QLabel('Ticker symbols for share'))
layout_tickers.addWidget(input_tickers)
layout_tickers.addLayout(layout_history_horizon)

gbox_tickers.setLayout(layout_tickers)

############### Methods Group ##################
layout_tools.addWidget(gbox_methods)
layout_methods = QGridLayout()

chbox_lrl = QCheckBox('LRL')
chbox_ma = QCheckBox('MA')
chbox_holt = QCheckBox('Holt')
chbox_exponential = QCheckBox('Exponential')
chbox_damped = QCheckBox('Damped')
chbox_arima = QCheckBox('ARIMA')
chbox_all = QCheckBox('All')

# Define signals and connect to events
checkboxes = [chbox_lrl, chbox_ma, chbox_holt, chbox_exponential, chbox_damped, chbox_arima]

def chbox_all_signal():
    for box in checkboxes:
        box.setChecked(True)

def chboxes_signal():
    if chbox_all.isChecked():
        chbox_all.setChecked(False)

chbox_all.clicked.connect(chbox_all_signal)
for chbox in checkboxes:
    chbox.clicked.connect(chboxes_signal)

layout_methods.addWidget(chbox_lrl, 0, 0)
layout_methods.addWidget(chbox_ma, 0, 1)
layout_methods.addWidget(chbox_holt, 0, 2)
layout_methods.addWidget(chbox_exponential, 1, 0)
layout_methods.addWidget(chbox_damped, 1, 1)
layout_methods.addWidget(chbox_arima, 1, 2)
layout_methods.addWidget(chbox_all, 0, 3)

gbox_methods.setLayout(layout_methods)

############## Indicators Group ################
layout_tools.addWidget(gbox_indicators)
layout_indicators = QGridLayout()

chbox_fibonacci = QCheckBox('Standard Fibonacci Retracements')
chbox_fibonacci_50 = QCheckBox('Fibonacci Retracements (50%)')
chbox_confidence = QCheckBox('Confidence Intervals')

layout_indicators.addWidget(chbox_fibonacci, 0, 0)
layout_indicators.addWidget(chbox_fibonacci_50, 1, 0)
layout_indicators.addWidget(chbox_confidence, 2, 0)

gbox_indicators.setLayout(layout_indicators)


################################################

tab_tools.setLayout(layout_tools)

tabs.addTab(tab_tools, 'Tools')

#################### GRAPH TAB #####################

tab_graph = QWidget()
layout_graph = QVBoxLayout()

df = yfinance.Ticker('ADA-USD').history('1y')
data = np.array( df['Close'] )
forecasts = libf.forecasts(data, ['arima'], 7, 7)

chartview = graphs.chart_view(data, forecasts)

layout_graph.addWidget(chartview)

layout_graph_buttons = QGridLayout()
btn_produce_graph = QPushButton('Produce Graph')
btn_save_graph = QPushButton('Save Graph')
layout_graph_buttons.addWidget(btn_produce_graph, 0, 0)
layout_graph_buttons.addWidget(btn_save_graph, 0, 1)

layout_graph.addLayout(layout_graph_buttons)

tab_graph.setLayout(layout_graph)
tabs.addTab(tab_graph, 'Graph')

###################################################
tab_indices = QWidget()

indices_layout = QVBoxLayout()

tab_indices.setLayout(indices_layout)

tabs.addTab(tab_indices, 'Indices')

tabs.setGeometry(0, 0, 900, 600)

tabs.show()

app.exec()