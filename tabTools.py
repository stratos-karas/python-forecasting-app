from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QComboBox, QSpinBox, QLabel, QCheckBox
import pandas as pd

class tabTools(QWidget):

    '''
    ========================
    --->>> Init class <<<---
    ========================
    '''
    def __init__(self):

        QWidget.__init__(self)

        # The main layout of the tools tab
        self.mainLayout = QVBoxLayout()

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
        self.mainLayout.addWidget(groupboxTickers)
        
        # The layout of the Tickers' GroupBox
        layoutTickers = QVBoxLayout()

        '''
        =======================
        --->>> First row <<<---
        =======================
        '''
        # The first row is a combination of a list
        # of the assets tickers and a text input
        self.inputTickers = QComboBox()
        self.inputTickers.setEditable(True)
        self.inputTickers.setDuplicatesEnabled(False)
        # Read a list of tickers from a csv file
        tickersNASDAQ = pd.read_csv('Tickers_NASDAQ.csv')[['Symbol', 'Name']]
        symbolNameNASDAQ = (tickersNASDAQ['Symbol'] + ', ' + tickersNASDAQ['Name']).tolist()
        # Insert ticker names to the inputTickers ComboBox
        self.inputTickers.insertItems(0, symbolNameNASDAQ)

        '''
        ========================
        --->>> Second row <<<---
        ========================
        '''
        # The layout of history, interval and horizon inputs
        layoutHistoryIntervalHorizon = QGridLayout()

        # History period input
        self.inputPeriod = QComboBox()
        self.inputPeriod.setEditable(False)
        self.inputPeriod.insertItems(0, ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'max'])

        # History interval input
        self.inputInterval = QComboBox()
        self.inputInterval.setEditable(False)
        self.inputInterval.insertItems(0, ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'])

        # Horizon input
        self.inputHorizon = QSpinBox()

        layoutHistoryIntervalHorizon.addWidget(QLabel('Period'), 0, 0)
        layoutHistoryIntervalHorizon.addWidget(self.inputPeriod, 1, 0)
        layoutHistoryIntervalHorizon.addWidget(QLabel('Interval'), 0, 1)
        layoutHistoryIntervalHorizon.addWidget(self.inputInterval, 1, 1)
        layoutHistoryIntervalHorizon.addWidget(QLabel("Horizon"), 0, 2)
        layoutHistoryIntervalHorizon.addWidget(self.inputHorizon, 1, 2)


        # Add first with second rows to tickers layout (tickers GroupBox)
        layoutTickers.addWidget(QLabel('Ticker symbols for share'))
        layoutTickers.addWidget(self.inputTickers)
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
        self.mainLayout.addWidget(groupboxMethods)
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
        self.checkboxes = [checkBoxLRL, checkBoxMA, checkBoxHolt, checkBoxExponential, checkBoxDamped, checkBoxARIMA]

        '''
        ============================
        --->>> Define Signals <<<---
        ============================
        '''
        # Check all the checkboxes inside
        # the list above
        def checkBoxAllEvent():
            for box in self.checkboxes:
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
        for chbox in self.checkboxes:
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

        self.mainLayout.addWidget(groupboxIndicators)
        layoutIndicators = QGridLayout()

        checkBoxFibonacci = QCheckBox('Standard Fibonacci Retracements')
        checkBoxFibonacci50 = QCheckBox('Fibonacci Retracements (50%)')
        checkBoxConfidence = QCheckBox('Confidence Intervals')

        layoutIndicators.addWidget(checkBoxFibonacci, 0, 0)
        layoutIndicators.addWidget(checkBoxFibonacci50, 1, 0)
        layoutIndicators.addWidget(checkBoxConfidence, 2, 0)

        groupboxIndicators.setLayout(layoutIndicators)

    '''
    =========================
    --->>> Get Methods <<<---
    =========================
    '''
    def getLayout(self):
        return self.mainLayout

    def getTicker(self):
        return self.inputTickers.currentText()

    def getPeriod(self):
        return self.inputPeriod.currentText()
    
    def getInterval(self):
        return self.inputInterval.currentText()

    def getHorizon(self):
        return self.inputHorizon.value()

    # TODO: Change it to return CHECKED checkboxes
    # rather than the whole checkboxes list (for privacy)
    def getCheckBoxes(self):
        return self.checkboxes