import datetime
from math import floor
from PyQt5.QtWidgets import QApplication, QGraphicsTextItem, QLineEdit, QTabWidget, QWidget,\
     QVBoxLayout, QGridLayout, QGroupBox, QComboBox, QSpinBox, QLabel, QCheckBox, QPushButton, QMainWindow, QGraphicsLineItem, QGraphicsRectItem

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QCategoryAxis, QValueAxis, QDateTimeAxis
from PyQt5.QtGui import QColor, QPainter, QCursor, QPainterPath, QPen, QFont
from PyQt5.QtCore import QDateTime, QEvent, QObject, QPoint, QPointF, Qt, QDate, QTime
import graphs
import yfinance
import libForecast as libf
import numpy as np
import pandas as pd

app = QApplication([])
app.setApplicationDisplayName("Forecasts for the poor")
app.setApplicationName("Forecasts for the poor")

tabs = QTabWidget()
tabs.setStyleSheet(
    " QTabWidget { color:white; background-color: #0a1429 } "
    " QTabBar { color:white; background-color: #0a1429 } "
    " QPushButton {color: white; background-color: #142952} "
    " QGroupBox {color: white; background-color: rgba(0, 15, 36, 0.91); border-radius: 5px; margin: 2px 0px;} "
    " QLabel {color: white} "
    " QCheckBox {color: white} "
    )

################ TAB TOOLS ###############
#region

tab_tools = QWidget()

# The main layout of the tools tab
layoutTools = QVBoxLayout()

# The 3 main divisions of the tabTools widget
groupboxTickers = QGroupBox('Tickers')
groupboxMethods = QGroupBox('Forecasting Methods')
groupboxIndicators = QGroupBox('Forecasting Indicators')


'''
*******************************************************
******************* Tickers GroupBox ******************
*******************************************************

- The input stage of the application

- A user should choose which asset he wants to forecast.
To choose an asset the specified ticker tied to the
asset is passed.

- A list of all publicly available assets should be
provided to the user as an alternative input method.

- A user can choose about the period of historical data,
the interval and the horizon of the forecast.

'''

# Tickers GroupBox is added to the main layout
layoutTools.addWidget(groupboxTickers)

# The layout of the Tickers' GroupBox
layoutTickers = QVBoxLayout()

'''
=======================
--->>> First row <<<---
=======================
'''
# The first row is a combination of a list
# of the assets tickers and a text input
inputTickers = QComboBox()
inputTickers.setEditable(True)
inputTickers.setDuplicatesEnabled(False)
# Read a list of tickers from a csv file
tickersNASDAQ = pd.read_csv('Tickers_NASDAQ.csv')[['Symbol', 'Name']]
symbolNameNASDAQ = (tickersNASDAQ['Symbol'] + ', ' + tickersNASDAQ['Name']).tolist()
# Insert ticker names to the inputTickers ComboBox
inputTickers.insertItems(0, symbolNameNASDAQ)

'''
========================
--->>> Second row <<<---
========================
'''
# The layout of history, interval and horizon inputs
layoutHistoryIntervalHorizon = QGridLayout()

# History period input
inputPeriod = QComboBox()
inputPeriod.setEditable(False)
inputPeriod.insertItems(0, ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'max'])

# History interval input
inputInterval = QComboBox()
inputInterval.setEditable(False)
inputInterval.insertItems(0, ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'])

# Horizon input
inputHorizon = QSpinBox()

layoutHistoryIntervalHorizon.addWidget(QLabel('Period'), 0, 0)
layoutHistoryIntervalHorizon.addWidget(inputPeriod, 1, 0)
layoutHistoryIntervalHorizon.addWidget(QLabel('Interval'), 0, 1)
layoutHistoryIntervalHorizon.addWidget(inputInterval, 1, 1)
layoutHistoryIntervalHorizon.addWidget(QLabel("Horizon"), 0, 2)
layoutHistoryIntervalHorizon.addWidget(inputHorizon, 1, 2)


# Add first with second rows to tickers layout (tickers GroupBox)
layoutTickers.addWidget(QLabel('Ticker symbols for share'))
layoutTickers.addWidget(inputTickers)
layoutTickers.addLayout(layoutHistoryIntervalHorizon)
# Everything is properly setup and
# we connect the layout to the Tickers' GroupBox widget
groupboxTickers.setLayout(layoutTickers)


'''
*******************************************************
******************* Methods GroupBox ******************
*******************************************************
'''

# Add Methods GroupBox to the main layout
layoutTools.addWidget(groupboxMethods)
# Create the layout of the Methods GroupBox
layoutMethods = QGridLayout()

# Create checkboxes
checkBoxLRL = QCheckBox('LRL')
checkBoxMA = QCheckBox('MA')
checkBoxHolt = QCheckBox('Holt')
checkBoxExponential = QCheckBox('Exponential')
checkBoxDamped = QCheckBox('Damped')
checkBoxARIMA = QCheckBox('ARIMA')
checkBoxAll = QCheckBox('All')

# List of checkboxes for signal functions
checkboxes = [checkBoxLRL, checkBoxMA, checkBoxHolt, checkBoxExponential, checkBoxDamped, checkBoxARIMA]

'''
============================
--->>> Define Signals <<<---
============================
'''
# Check all the checkboxes inside
# the list above
def checkBoxAllEvent():
    for box in checkboxes:
        box.setChecked(True)

# If a checkbox was checked then
# un-check the "All" checkbox
def checkBoxChecked():
    if checkBoxAll.isChecked():
        checkBoxAll.setChecked(False)

'''
=======================================
--->>> Connect events to signals <<<---
=======================================
'''
# If "All" checkbox is clicked(event) then
# check all the checkboxes
checkBoxAll.clicked.connect(checkBoxAllEvent)

# If any checkbox from the list is clicked
# (event) the "All" checkbox is un-checked
for chbox in checkboxes:
    chbox.clicked.connect(checkBoxChecked)

layoutMethods.addWidget(checkBoxLRL, 0, 0)
layoutMethods.addWidget(checkBoxMA, 0, 1)
layoutMethods.addWidget(checkBoxHolt, 0, 2)
layoutMethods.addWidget(checkBoxExponential, 1, 0)
layoutMethods.addWidget(checkBoxDamped, 1, 1)
layoutMethods.addWidget(checkBoxARIMA, 1, 2)
layoutMethods.addWidget(checkBoxAll, 0, 3)

groupboxMethods.setLayout(layoutMethods)


'''
*******************************************************
****************** Indicators GroupBox ****************
*******************************************************
'''

layoutTools.addWidget(groupboxIndicators)
layoutIndicators = QGridLayout()

checkBoxFibonacci = QCheckBox('Standard Fibonacci Retracements')
checkBoxFibonacci50 = QCheckBox('Fibonacci Retracements (50%)')
checkBoxConfidence = QCheckBox('Confidence Intervals')

layoutIndicators.addWidget(checkBoxFibonacci, 0, 0)
layoutIndicators.addWidget(checkBoxFibonacci50, 1, 0)
layoutIndicators.addWidget(checkBoxConfidence, 2, 0)

groupboxIndicators.setLayout(layoutIndicators)

tab_tools.setLayout(layoutTools)

tabs.addTab(tab_tools, 'Tools')

#endregion

#################### GRAPH TAB #####################

tabGraph = QWidget()
layoutGraph = QVBoxLayout()

# dataSeriesValue = QLineEdit("Value of the series will be visible here")
# layoutGraph.addWidget(dataSeriesValue)

painter = QPainter()

chart = QChart()
chart.setTheme(QChart.ChartThemeDark)
chart.createDefaultAxes()
chart.setAnimationOptions(QChart.SeriesAnimations)
chart.legend().setVisible(True)

chartView = QChartView(chart)
scene = chartView.scene()
chartView.setRenderHint(painter.Antialiasing)
chartView.setStyleSheet("background-color: rgba(0.0, 0.0, 0.0, 0.0); border-radius: 5px")
chartView.setCursor(Qt.CrossCursor)

pen = QPen()
# pen.setWidth(10)
# pen.setColor(QColor(255, 255, 255, 175))
chartViewCursorLine = QGraphicsLineItem(0, 0, 0, 0, None)
scene.addItem(chartViewCursorLine)
chartViewValueText = QGraphicsTextItem("")
chartViewValueText.setDefaultTextColor(QColor(255, 255, 255, 255))
scene.addItem(chartViewValueText)
def dataSeriesHovered(dataSeries):
    global pen
    pen.setColor(dataSeries.color())
    
    global chartViewCursorLine
    scene.removeItem(chartViewCursorLine)
    chartViewCursorLine = QGraphicsLineItem(chartView.mapFromGlobal(QCursor.pos()).x(), chart.plotArea().top(), chartView.mapFromGlobal(QCursor.pos()).x(), chart.plotArea().top() + chart.plotArea().height())
    chartViewCursorLine.setPen(pen)
    scene.addItem(chartViewCursorLine)

    global chartViewValueText
    scene.removeItem(chartViewValueText)
    chartViewValueText = QGraphicsTextItem(str(chart.mapToValue(chartView.mapFromGlobal(QCursor.pos()), dataSeries).y()))
    chartViewValueText.setDefaultTextColor(dataSeries.color())
    chartViewValueText.setPos(chartView.mapFromGlobal(QCursor.pos()).x(), chart.plotArea().top() - 22)
    scene.addItem(chartViewValueText)
    # chartView.scene().addSimpleText(str(chart.mapToValue(chartView.mapFromGlobal(QCursor.pos()), dataSeries).y()), QFont())
    # dataSeriesValue.setText(str(chart.mapToValue(chartView.mapFromGlobal(QCursor.pos()), dataSeries).y()))

layoutGraph.addWidget(chartView)

layoutGraphButtons = QGridLayout()

# def test_func(poinAreaWidth, series):
#     chartPosition = chartView.viewport().mapFromGlobal(QCursor.pos())
#     seriesIndex = chartPosition.x() / poinAreaWidth
#     print(series.at(seriesIndex))

def test_func(data):
    mouseToAxisPosition = chart.mapToValue(QCursor.pos(), data).x()
    pointValue = data.at(floor(mouseToAxisPosition)).y()
    # painter.setPen(QPen(Qt.red))
    painterPath = scene.selectionArea()
    painterPath.addText(chart.mapToPosition(QCursor.pos(), data), QFont(),str(pointValue))

def produce_graph_clicked():
    
    # Remove the previous axis to redraw the new ones
    allAxes = []
    for series in chart.series():
        allAxes.append( series.attachedAxes() )
        # allAxes.append( chart.axes(Qt.Orientation.Horizontal) )
        # allAxes.append( chart.axes(Qt.Orientation.Vertical) )

    for axis in allAxes:
        chart.removeAxis(axis[0])
        chart.removeAxis(axis[1])

    # Cleanup all the drawn series
    # TODO: remove only the forecasts not the historical data line

    chart.removeAllSeries()
    
    # Read the ticker symbol of the asset we want to forecast
    tickerSymbol = inputTickers.currentText().split(',')[0]
    # Add title to the chart
    chart.setTitle(tickerSymbol + " Forecasting")
    
    dataFrame = yfinance.Ticker(tickerSymbol).history(inputPeriod.currentText())
    dataClose = np.array( dataFrame['Close'] )
    # data_open = np.array( dataFrame['Open'] )

    # Get forecasting methods from the checkboxes
    forecastingMethods = []
    for box in checkboxes:
        if box.isChecked():
            forecastingMethods.append(box.text().lower())

    # Get forecasts
    forecasts = libf.forecasts(dataClose, forecastingMethods, 7, inputHorizon.value())

    dateIndex = dataFrame.index
    dates = [str(val.date()) for val in dateIndex] + [str(dateIndex[-1].date() + datetime.timedelta(days=i)) for i in range(1, forecasts['Horizon']+1)]
    
    Qdates = []
    for date in dates:
        dateSplit = date.split('-')
        datetimeValue = QDateTime()
        datetimeValue.setDate(QDate(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2])))
        Qdates.append(datetimeValue)

    axisX = QDateTimeAxis()
    axisX.setRange(Qdates[0], Qdates[-1])
    axisX.setFormat("dd-MM-yy")
    # axisX.setLabelsAngle(-30)

    axisY = QValueAxis()
    axisY.setRange(dataClose.min() - dataClose.min()/50, dataClose.max() + dataClose.max()/50)
    axisY.setMinorTickCount(5)

    chart.addAxis(axisX, Qt.AlignBottom)
    chart.addAxis(axisY, Qt.AlignLeft)

    # Create and Draw the Historical data series
    historicalData = QLineSeries()
    historicalData.setName("Historical Data")
    for idx in range( len(dataClose) ):
        historicalData.append(Qdates[idx].toMSecsSinceEpoch(), dataClose[idx])
    # historicalData.append(len(dataClose).toMSecsSinceEpoch(), for)


    chart.addSeries(historicalData)

    historicalData.attachAxis(axisX)
    historicalData.attachAxis(axisY)

    historicalData.hovered.connect(lambda: dataSeriesHovered(historicalData))
    # for point in series.pointsVector():
    #     seriesMappedToPixels.append((chartView.viewport().mapFromGlobal(QPoint(int(point.x()), int(point.y()))).x(), point.y()))

    # Create and draw the forecasting methods
    for method in forecastingMethods:

        forecastingData = QLineSeries()
        forecastingData.setName(method.capitalize())
        forecastingData.append(Qdates[(len(dataClose) - 1)].toMSecsSinceEpoch(), dataClose[-1])
        time = [t for t in range(len(dataClose), len(dataClose) + forecasts['Horizon'] + 1)]
        
        for idx in range( forecasts['Horizon'] ):
            forecastingData.append(Qdates[time[idx]].toMSecsSinceEpoch(), forecasts[method][idx])
        
        chart.addSeries(forecastingData)
        
        forecastingData.hovered.connect(lambda: dataSeriesHovered(forecastingData))
        forecastingData.attachAxis(axisX)
        forecastingData.attachAxis(axisY)


    # Create axes based off the data we feed it
    # historicalData.clicked.connect(lambda: test_func(historicalData))
    # chart.createDefaultAxes()




btn_produce_graph = QPushButton('Produce Graph')
btn_produce_graph.clicked.connect(produce_graph_clicked)

btn_save_graph = QPushButton('Save Graph')

layoutGraphButtons.addWidget(btn_produce_graph, 0, 0)
layoutGraphButtons.addWidget(btn_save_graph, 0, 1)

layoutGraph.addLayout(layoutGraphButtons)

tabGraph.setLayout(layoutGraph)
tabs.addTab(tabGraph, 'Graph')

###################################################
tab_indices = QWidget()

indices_layout = QVBoxLayout()

tab_indices.setLayout(indices_layout)

tabs.addTab(tab_indices, 'Indices')

tabs.setGeometry(0, 0, 900, 600)

tabs.show()

app.exec()