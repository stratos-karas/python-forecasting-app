from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPainter

def chart_view(data, forecasts):
    
    series = QLineSeries()
    for idx in range( len(data) ):
        series.append(idx, data[idx])

    fseries = QLineSeries()
    time = [t for t in range(len(data) - 1, len(data) + forecasts['Horizon'])]
    for idx in range( forecasts['Horizon'] ):
        fseries.append(time[idx], forecasts['ARIMA'][idx])


    chart = QChart()
    chart.setTheme(QChart.ChartThemeDark)
    # chart.setBackgroundVisible(False)

    chart.addSeries(series)
    chart.addSeries(fseries)
    chart.createDefaultAxes()
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.legend().setVisible(True)

    chartview = QChartView(chart)
    chartview.setRenderHint(QPainter.Antialiasing)

    return chartview